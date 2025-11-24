output "instance_ids" {
  value       = [for instance in local.instances : instance.id]
  description = "Lista de IDs de instancias"
}

output "instance_ips" {
  value       = [for instance in local.instances : instance.private_ip]
  description = "IPs privadas de las instancias"
}

output "instance_count" {
  value       = var.instance_count
  description = "Número de instancias creadas"
}

output "instance_type" {
  value       = var.instance_type
  description = "Tipo de instancia utilizado"
}
