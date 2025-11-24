variable "bucket_name" {
  type        = string
  description = "Nombre del bucket de almacenamiento"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.bucket_name))
    error_message = "El nombre del bucket solo puede contener letras minúsculas, números y guiones."
  }
}

variable "versioning_enabled" {
  type        = bool
  description = "Habilitar versionado"
  default     = false
}

variable "encryption_enabled" {
  type        = bool
  description = "Habilitar encriptación"
  default     = true
}

variable "tags" {
  type        = map(string)
  description = "Tags para el bucket"
  default     = {}
}
