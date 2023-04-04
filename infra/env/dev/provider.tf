terraform {
  required_version = ">= 1.0.2"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
  backend "local" {
    path = "/home/john/terraform.tfstate"
  }
}

provider "aws" {
  region = var.region
}

module "api" {
  source = "../../modules/api-gateway"
  region = var.region
  lambda_security_group_id = ""
  lambda_subnet_ids = []
  project_name = var.project_name
}

module "network" {
  source = "../../modules/network"
  project_name = var.project_name
}
