locals {
  zone_id     = "zone-${md5(var.zone_name)}"
  dns_mapping = zipmap(var.hostnames, var.ip_addresses)
}

# Simulación de zona DNS
resource "null_resource" "dns_zone" {
  triggers = {
    zone_name = var.zone_name
  }
}

# Simulación de registros DNS
resource "null_resource" "dns_records" {
  count = length(var.hostnames)

  triggers = {
    hostname   = var.hostnames[count.index]
    ip_address = var.ip_addresses[count.index]
    zone_id    = local.zone_id
  }

  depends_on = [null_resource.dns_zone]
}
