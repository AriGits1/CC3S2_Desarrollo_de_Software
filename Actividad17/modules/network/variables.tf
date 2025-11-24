variable "vpc_cidr" {
  type        = string
  description = "CIDR block para la VPC"
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "El CIDR debe ser válido."
  }
}

variable "subnet_count" {
  type        = number
  description = "Número de subnets a crear"
  default     = 2

  validation {
    condition     = var.subnet_count > 0 && var.subnet_count <= 10
    error_message = "El número de subnets debe estar entre 1 y 10."
  }
}

variable "environment" {
  type        = string
  description = "Nombre del entorno"
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "El entorno debe ser dev, staging o prod."
  }
}

variable "availability_zones" {
  type        = list(string)
  description = "Lista de zonas de disponibilidad"
  default     = ["us-east-1a", "us-east-1b"]
}
