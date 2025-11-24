output "bucket_id" {
  value       = local.bucket_id
  description = "ID del bucket"
}

output "bucket_arn" {
  value       = local.bucket_arn
  description = "ARN del bucket"
}

output "bucket_name" {
  value       = var.bucket_name
  description = "Nombre del bucket"
}

output "bucket_region" {
  value       = local.bucket_region
  description = "Región del bucket"
}

output "versioning_status" {
  value       = var.versioning_enabled ? "Enabled" : "Disabled"
  description = "Estado del versionado"
}
