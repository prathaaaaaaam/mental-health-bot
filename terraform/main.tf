terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# NOTE: This is a student skeleton. You can plug in community modules later.
# VPC, EKS, and NodeGroup modules can be added here.
# For now, we just create an S3 bucket for state demo.

resource "aws_s3_bucket" "artifact_bucket" {
  bucket = "${var.project}-artifacts-${random_id.rand.hex}"
}

resource "random_id" "rand" {
  byte_length = 4
}