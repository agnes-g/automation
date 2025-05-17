variable "vpc_name" {
  description = "VPC name"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC cidr"
  type        = string
}

variable "vpc_azs" {
  description = "Subnet availability zones"
  type        = list(string)
}

variable "vpc_public_subnets" {
  description = "Public subnets"
  type        = list(string)
}

variable "instance_name" {
  description = "EC2 instance name"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}