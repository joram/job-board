variable "env" {
  description = "(Required) The current running environment"
  type        = string
  default = "dev"
}

variable "project_name" {
  description = "(Required) Name of the project, used for top level resources and tagging"
  type        = string
  default = "job-board-dev"
}

variable "region" {
  description = "(Required) The region to build infra in"
  type        = string
    default = "ca-central-1"
}
