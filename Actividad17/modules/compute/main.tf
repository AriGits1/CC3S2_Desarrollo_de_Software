locals {
  instances = [
    for i in range(var.instance_count) : {
      id         = "i-${md5("${var.ami_id}-${i}")}"
      private_ip = cidrhost(var.subnet_ids[i % length(var.subnet_ids)], i + 10)
      subnet_id  = var.subnet_ids[i % length(var.subnet_ids)]
    }
  ]
}

# Simulación de instancias
resource "null_resource" "instances" {
  count = var.instance_count

  triggers = {
    instance_type = var.instance_type
    subnet_id     = local.instances[count.index].subnet_id
    ami_id        = var.ami_id
  }
}
