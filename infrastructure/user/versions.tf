terraform {
  required_version = "~>1.11.4"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.97.0"
    }
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      "ManagedByTerraform" : true,
      "Source" : "infrastructure/user"
      "Repository" : "agnes-g/automation"
    }
  }
}
