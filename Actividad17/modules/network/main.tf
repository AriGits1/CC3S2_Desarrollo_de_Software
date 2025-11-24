locals {
  vpc_id         = "vpc-${md5(var.vpc_cidr)}"
  route_table_id = "rtb-${md5(var.vpc_cidr)}"
  
  subnets = [
    for i in range(var.subnet_count) : {
      id   = "subnet-${md5("${var.vpc_cidr}-${i}")}"
      cidr = cidrsubnet(var.vpc_cidr, 8, i)
      az   = var.availability_zones[i % length(var.availability_zones)]
    }
  ]
}

# Simulación de recursos (sin proveedores reales)
resource "null_resource" "vpc" {
  triggers = {
    vpc_cidr    = var.vpc_cidr
    environment = var.environment
  }
}

resource "null_resource" "subnets" {
  count = var.subnet_count

  triggers = {
    subnet_cidr = local.subnets[count.index].cidr
    vpc_id      = local.vpc_id
  }

  depends_on = [null_resource.vpc]
}
