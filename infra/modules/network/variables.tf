variable "vpc_cidr_block" {
  description = "(Optional) The VPC's CIDR block"
  default     = "10.16.0.0/16"
  type        = string
}

variable "region" {
  default = "ca-central-1"
}

variable "project_name" {
  default = ""
}