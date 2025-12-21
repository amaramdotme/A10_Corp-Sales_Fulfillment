variable "resource_group_name" {
  description = "The name of the resource group containing the existing network resources."
  type        = string
}

variable "location" {
  description = "The Azure region where the resources will be deployed."
  type        = string
}

variable "cluster_name" {
  description = "The name of the AKS cluster."
  type        = string
}

variable "dns_prefix" {
  description = "DNS prefix for the AKS cluster."
  type        = string
}

variable "kubernetes_version" {
  description = "The version of Kubernetes to use."
  type        = string
  default     = "1.32" 
}

variable "vnet_name" {
  description = "The name of the existing Virtual Network."
  type        = string
}

variable "subnet_name" {
  description = "The name of the existing Subnet for AKS nodes."
  type        = string
}

variable "identity_name" {
  description = "The name of the existing User Assigned Identity for the AKS Control Plane."
  type        = string
}

variable "node_count" {
  description = "The initial number of nodes for the default node pool."
  type        = number
  default     = 2
}

variable "vm_size" {
  description = "The VM size for the default node pool."
  type        = string
  default     = "Standard_D2s_v3"
}

variable "tags" {
  description = "A mapping of tags to assign to the resource."
  type        = map(string)
  default     = {}
}

# Networking - Defaults chosen to avoid 10.0.0.0/16 VNet overlap
variable "service_cidr" {
  description = "The CIDR to use for Kubernetes services (must not overlap with VNet)."
  type        = string
  default     = "172.16.0.0/16"
}

variable "dns_service_ip" {
  description = "IP address within the Kubernetes service CIDR to use for DNS."
  type        = string
  default     = "172.16.0.10"
}