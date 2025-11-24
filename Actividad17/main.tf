# Ejemplo de integración de módulos
# Este archivo demuestra cómo usar los módulos juntos

terraform {
  required_version = ">= 1.0"
}

# Módulo de red (base)
module "network" {
  source = "./modules/network"

  vpc_cidr            = "10.0.0.0/16"
  subnet_count        = 2
  environment         = "dev"
  availability_zones  = ["us-east-1a", "us-east-1b"]
}

# Módulo de firewall (depende de network)
module "firewall" {
  source = "./modules/firewall"

  vpc_id        = module.network.vpc_id
  allowed_ports = [80, 443, 22]
  allowed_cidrs = ["10.0.0.0/16", "192.168.1.0/24"]
}

# Módulo de cómputo (depende de network)
module "compute" {
  source = "./modules/compute"

  subnet_ids     = module.network.subnet_ids
  instance_count = 2
  instance_type  = "t2.micro"
  ami_id         = "ami-0c55b159cbfafe1f0"
}

# Módulo de DNS (depende de compute)
module "dns" {
  source = "./modules/dns"

  hostnames    = ["web.example.com", "api.example.com"]
  ip_addresses = module.compute.instance_ips
  zone_name    = "example.com"
}

# Módulo de almacenamiento (independiente)
module "storage" {
  source = "./modules/storage"

  bucket_name         = "my-app-bucket-${module.network.vpc_id}"
  versioning_enabled  = true
  encryption_enabled  = true

  tags = {
    Environment = "dev"
    Project     = "test-iac"
  }
}

# Outputs de la integración
output "infrastructure_summary" {
  value = {
    vpc_id         = module.network.vpc_id
    subnet_count   = length(module.network.subnet_ids)
    instance_count = module.compute.instance_count
    dns_records    = length(keys(module.dns.dns_mapping))
    firewall_rules = module.firewall.rules_count
    storage_bucket = module.storage.bucket_name
  }
  description = "Resumen de la infraestructura desplegada"
}

output "dns_configuration" {
  value       = module.dns.dns_mapping
  description = "Mapeo de hostnames a IPs"
}

output "firewall_policy" {
  value       = module.firewall.firewall_policy
  description = "Política de firewall en JSON"
  sensitive   = false
}
