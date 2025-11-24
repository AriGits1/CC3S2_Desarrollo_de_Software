locals {
  security_group_id = "sg-${md5(var.vpc_id)}"
  
  firewall_rules = [
    for idx, port in var.allowed_ports : {
      rule_id     = "rule-${idx + 1}"
      port        = port
      protocol    = "tcp"
      allowed_ips = var.allowed_cidrs
      action      = "allow"
    }
  ]
}

# Simulación de security group
resource "null_resource" "security_group" {
  triggers = {
    vpc_id      = var.vpc_id
    rules_count = length(var.allowed_ports)
  }
}

resource "null_resource" "security_rules" {
  count = length(var.allowed_ports)

  triggers = {
    port  = var.allowed_ports[count.index]
    cidrs = join(",", var.allowed_cidrs)
  }

  depends_on = [null_resource.security_group]
}
