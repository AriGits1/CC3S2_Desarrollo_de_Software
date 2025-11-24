output "dns_mapping" {
  value       = local.dns_mapping
  description = "Mapa de hostname->IP"
}

output "zone_id" {
  value       = local.zone_id
  description = "ID de la zona DNS"
}

output "records_count" {
  value       = length(var.hostnames)
  description = "Número de registros DNS creados"
}

output "zone_name" {
  value       = var.zone_name
  description = "Nombre de la zona DNS"
}
