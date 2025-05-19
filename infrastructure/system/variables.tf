variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "eventbridge_bus_name" {
  description = "Name of the event bus"
  type        = string
  default = "default"
}


variable "lambda_name" {
  description = "Lambda name"
  type = string
  default = "security-ssm-enable-lambda"
}

variable "lambda_runtime" {
  description = "Lambda runtime"
  type = string
  default = "python3.13"
}

variable "lambda_timeout" {
  description = "Lambda timeout"
  type = number
  default = 30
}

variable "lambda_description" {
  description = "The description of lambda"
  type = string
  default = "Attaches an IAM policy to EC2 instance profile role"
}

variable "lambda_handler" {
  type = string
  default = "policy_attach.lambda_handler"
}

variable "lambda_s3_key" {
  type = string
  default = "artifact/lambda.zip"
}

variable "lambda_policy_to_attach" {
  type = string
  default = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

variable "default_instance_profile_name" {
  type = string
  default = "default-ssm-instance-profile"
}