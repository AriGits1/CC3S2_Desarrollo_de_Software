output "vpc_id" {
  value       = local.vpc_id
  description = "ID de la VPC creada"
}

output "subnet_ids" {
  value       = [for subnet in local.subnets : subnet.id]
  description = "Lista de IDs de subnets"
}

output "vpc_cidr_block" {
  value       = var.vpc_cidr
  description = "CIDR block de la VPC"
}

output "route_table_id" {
  value       = local.route_table_id
  description = "ID de la tabla de rutas"
}

output "subnet_cidrs" {
  value       = [for subnet in local.subnets : subnet.cidr]
  description = "Lista de CIDR blocks de subnets"
}
