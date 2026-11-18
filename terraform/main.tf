terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region  = "ap-south-1"
  profile = "personal"
}

resource "aws_s3_bucket" "bankflow" {
  bucket = "bankflow-data-etl-bucket-002"

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    Project = "BankFlow"
    ManagedBy = "Terraform"
  }
}