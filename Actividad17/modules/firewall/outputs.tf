output "firewall_policy" {
  value = jsonencode({
    version = "1.0"
    rules   = local.firewall_rules
  })
  description = "Política de firewall en formato JSON"
}

output "security_group_id" {
  value       = local.security_group_id
  description = "ID del grupo de seguridad"
}

output "rules_count" {
  value       = length(var.allowed_ports)
  description = "Número de reglas aplicadas"
}
