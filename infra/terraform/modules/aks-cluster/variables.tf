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
  default     = "1.32" # Bumped to 1.32 to avoid LTS errors
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
  default     = "Standard_B2s" # Cost-optimized for dev/stage
}

variable "tags" {
  description = "A mapping of tags to assign to the resource."
  type        = map(string)
  default     = {}
}
