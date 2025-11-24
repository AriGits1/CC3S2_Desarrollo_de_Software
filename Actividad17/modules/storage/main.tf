locals {
  bucket_id   = "bucket-${md5(var.bucket_name)}"
  bucket_arn  = "arn:aws:s3:::${var.bucket_name}"
  bucket_region = "us-east-1"
}

# Simulación de bucket
resource "null_resource" "bucket" {
  triggers = {
    bucket_name        = var.bucket_name
    versioning_enabled = var.versioning_enabled
    encryption_enabled = var.encryption_enabled
  }
}

resource "null_resource" "bucket_policy" {
  count = var.encryption_enabled ? 1 : 0

  triggers = {
    bucket_id = local.bucket_id
    policy    = "encryption-required"
  }

  depends_on = [null_resource.bucket]
}
