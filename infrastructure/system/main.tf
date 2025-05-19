module "s3_bucket" {
  source = "terraform-aws-modules/s3-bucket/aws"

  bucket = var.lambda_name
  acl    = "private"

  control_object_ownership = true
  object_ownership         = "ObjectWriter"

  versioning = {
    enabled = true
  }
}

data aws_iam_policy_document "attach_ssm_policy_document" {
  statement {
    sid    = "readEC2InstanceProfile"
    effect = "Allow"
    actions = [
      "iam:GetInstanceProfile"
    ]
    resources = ["*"]
  }

  statement {
    sid    = "attachSSMPolicy"
    effect = "Allow"
    actions = [
      "iam:AttachRolePolicy"
    ]
    resources = ["*"]

    condition {
      test     = "StringEquals"
      values = [var.lambda_policy_to_attach]
      variable = "iam:PolicyARN"
    }
  }

  statement {
    sid    = "attachInstanceProfile"
    effect = "Allow"
    actions = [
      "ec2:AssociateIamInstanceProfile",
      "iam:PassRole" # todo MUST NOT BE WILDCARD
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "lambda_iam_policy" {
  policy = data.aws_iam_policy_document.attach_ssm_policy_document.json
  name_prefix = var.lambda_name
}

module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.21.0"

  function_name = var.lambda_name
  description   = var.lambda_description
  handler       = var.lambda_handler
  runtime       = var.lambda_runtime

  create_package = false
  publish = true

  attach_policy = true
  policy = aws_iam_policy.lambda_iam_policy.arn

  environment_variables = {
    DEFAULT_INSTANCE_PROFILE_NAME = module.default_instance_role.instance_profile_name
  }

  timeout = var.lambda_timeout

  s3_existing_package = {
    bucket = module.s3_bucket.s3_bucket_id
    key    = var.lambda_s3_key
  }

  allowed_triggers = {
    for k, rule in module.eventbridge.eventbridge_rules : k =>
    {
      principal  = "events.amazonaws.com"
      source_arn = rule.arn
    }
  }
}

module "eventbridge" {
  source  = "terraform-aws-modules/eventbridge/aws"
  version = "3.16.0"

  bus_name = var.eventbridge_bus_name
  create_bus = var.eventbridge_bus_name != "default"

  rules = {
    instances = {
      description = "Capture ec2 RunInstances events"
      event_pattern = jsonencode({
        "source" : ["aws.ec2"]
        "detail-type" : ["AWS API Call via CloudTrail"]
        "detail" : {
          "eventSource" : ["ec2.amazonaws.com"],
          "eventName" : ["RunInstances"]
        }
      })
      role_arn: true
    }
  }

  targets = {
    instances = [
      {
        name = "invoke-security-lambda"
        arn  = module.lambda_function.lambda_function_arn
        attach_role_arn: true
      }
    ]
  }

  create_role = true
  attach_lambda_policy = true
  lambda_target_arns = [module.lambda_function.lambda_function_arn]
}

module "default_instance_role" {
  source = "../../modules/instance-role"
  instance_profile_name = var.default_instance_profile_name
}