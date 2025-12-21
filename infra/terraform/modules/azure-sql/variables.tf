variable "resource_group_name" {
  description = "The name of the resource group."
  type        = string
}

variable "location" {
  description = "The Azure region."
  type        = string
}

variable "server_name" {
  description = "The name of the Azure SQL Server."
  type        = string
}

variable "database_name" {
  description = "The name of the Azure SQL Database."
  type        = string
}

variable "admin_username" {
  description = "The administrator username for the SQL Server."
  type        = string
}

variable "admin_password" {
  description = "The administrator password for the SQL Server."
  type        = string
  sensitive   = true
}

variable "sku_name" {
  description = "The SKU for the database (e.g., S0, GP_Gen5_2, Basic)."
  type        = string
  default     = "Basic"
}

variable "aks_subnet_id" {
  description = "The resource ID of the AKS subnet to allow access from."
  type        = string
}

variable "tags" {
  description = "A mapping of tags to assign to the resource."
  type        = map(string)
  default     = {}
}

variable "allow_public_access" {
  description = "Whether to allow public access to the SQL Server."
  type        = bool
  default     = false
}

variable "public_ip" {
  description = "A public IP address to allow access from (only if allow_public_access is true)."
  type        = string
  default     = null
}

