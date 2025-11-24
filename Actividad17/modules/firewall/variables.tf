variable "allowed_ports" {
  type        = list(number)
  description = "Lista de puertos permitidos"

  validation {
    condition = alltrue([
      for port in var.allowed_ports : port >= 1 && port <= 65535
    ])
    error_message = "Los puertos deben estar entre 1 y 65535."
  }
}

variable "allowed_cidrs" {
  type        = list(string)
  description = "Lista de CIDRs permitidos"

  validation {
    condition = alltrue([
      for cidr in var.allowed_cidrs : can(cidrhost(cidr, 0))
    ])
    error_message = "CIDRs mal formados detectados."
  }
}

variable "vpc_id" {
  type        = string
  description = "ID de la VPC"
}
