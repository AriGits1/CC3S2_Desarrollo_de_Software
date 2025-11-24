variable "subnet_ids" {
  type        = list(string)
  description = "Lista de subnets donde desplegar instancias"
}

variable "instance_count" {
  type        = number
  description = "Número de instancias a crear"
  default     = 2

  validation {
    condition     = var.instance_count > 0 && var.instance_count <= 20
    error_message = "El número de instancias debe estar entre 1 y 20."
  }
}

variable "instance_type" {
  type        = string
  description = "Tipo de instancia"
  default     = "t2.micro"

  validation {
    condition     = contains(["t2.micro", "t2.small", "t2.medium"], var.instance_type)
    error_message = "El tipo de instancia debe ser t2.micro, t2.small o t2.medium."
  }
}

variable "ami_id" {
  type        = string
  description = "ID de la AMI a utilizar"
  default     = "ami-12345678"
}
