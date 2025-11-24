variable "hostnames" {
  type        = list(string)
  description = "Lista de nombres de host"

  validation {
    condition = alltrue([
      for hostname in var.hostnames : can(regex("^[a-zA-Z0-9.-]+$", hostname))
    ])
    error_message = "Los hostnames solo pueden contener letras, números, puntos y guiones."
  }

  validation {
    condition = alltrue([
      for hostname in var.hostnames : !can(regex(" ", hostname))
    ])
    error_message = "Los hostnames no pueden contener espacios."
  }
}

variable "ip_addresses" {
  type        = list(string)
  description = "Lista de direcciones IP"

  validation {
    condition     = length(var.hostnames) == length(var.ip_addresses)
    error_message = "El número de hostnames debe coincidir con el número de IPs."
  }
}

variable "zone_name" {
  type        = string
  description = "Nombre de la zona DNS"
  default     = "example.com"
}
