# Data sources to lookup existing infrastructure
data "azurerm_resource_group" "rg" {
  name = var.resource_group_name
}

data "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  resource_group_name = data.azurerm_resource_group.rg.name
}

data "azurerm_subnet" "aks_subnet" {
  name                 = var.subnet_name
  virtual_network_name = data.azurerm_virtual_network.vnet.name
  resource_group_name  = data.azurerm_resource_group.rg.name
}

data "azurerm_user_assigned_identity" "aks_identity" {
  name                = var.identity_name
  resource_group_name = data.azurerm_resource_group.rg.name
}

# AKS Cluster Resource
resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.cluster_name
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  dns_prefix          = var.dns_prefix
  kubernetes_version  = var.kubernetes_version

  default_node_pool {
    name           = "default"
    node_count     = var.node_count
    vm_size        = var.vm_size
    vnet_subnet_id = data.azurerm_subnet.aks_subnet.id
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [data.azurerm_user_assigned_identity.aks_identity.id]
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
    service_cidr      = var.service_cidr
    dns_service_ip    = var.dns_service_ip
  }

  tags = var.tags
}

# Grant AcrPull to the Kubelet Identity
resource "azurerm_role_assignment" "acr_pull" {
  scope                = var.acr_id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
}

# Grant Storage Blob Data Contributor to the Kubelet Identity
resource "azurerm_role_assignment" "storage_contributor" {
  scope                = var.storage_account_id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
}

# Add NSG rules to the existing NSG for the node pool
resource "azurerm_network_security_rule" "allow_http" {
  name                        = "AllowHttpInboundFromInternet"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "80"
  source_address_prefix       = "Internet"
  destination_address_prefix  = "*"
  resource_group_name         = data.azurerm_resource_group.rg.name
  network_security_group_name = var.node_nsg_name
}

resource "azurerm_network_security_rule" "allow_lb_probes" {
  name                        = "AllowAzureLBInbound"
  priority                    = 110
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "AzureLoadBalancer"
  destination_address_prefix  = "*"
  resource_group_name         = data.azurerm_resource_group.rg.name
  network_security_group_name = var.node_nsg_name
}

# ============================================================================
# TEMPORARY: Storage Account Network Configuration
# ============================================================================
# TODO: Move this to Foundation repo (A10_Corp-terraform)
# This configuration should be owned by the Platform team, not the workload.
#
# Why it's here temporarily:
# - Poly-repo architecture: Foundation creates storage account, but doesn't
#   know about workload-specific AKS subnets at provision time
# - Need to enable service endpoints for AKS pods to access blob storage
#
# Proper solution:
# 1. Foundation repo should manage storage account network rules
# 2. Foundation repo should enable service endpoints on subnets it creates
# 3. This repo should only reference the storage account (data source)
# ============================================================================

# Extract storage account details from resource ID
locals {
  storage_account_id_parts = split("/", var.storage_account_id)
  storage_rg_name          = local.storage_account_id_parts[4]
  storage_account_name     = local.storage_account_id_parts[8]
  storage_subscription_id  = local.storage_account_id_parts[2]
}

# Enable Microsoft.Storage service endpoint on AKS subnet
# NOTE: This modifies a subnet managed by Foundation - should move there
resource "null_resource" "enable_service_endpoint" {
  triggers = {
    subnet_id = data.azurerm_subnet.aks_subnet.id
  }

  provisioner "local-exec" {
    command = <<-EOT
      az network vnet subnet update \
        --ids ${data.azurerm_subnet.aks_subnet.id} \
        --service-endpoints Microsoft.Storage
    EOT
  }

  depends_on = [azurerm_kubernetes_cluster.aks]
}

# Data source for storage account
data "azurerm_storage_account" "backup_storage" {
  name                = local.storage_account_name
  resource_group_name = local.storage_rg_name
}

# Configure storage account to accept traffic from AKS subnet
# NOTE: This manages resources in the Foundation subscription - should move there
# WARNING: This will replace ALL existing network rules (including any manual IP rules)
resource "azurerm_storage_account_network_rules" "allow_aks_access" {
  storage_account_id = var.storage_account_id

  default_action             = "Deny"
  bypass                     = ["AzureServices"]
  virtual_network_subnet_ids = [data.azurerm_subnet.aks_subnet.id]

  # No IP rules - use service endpoint for AKS access
  # For portal access, temporarily set defaultAction=Allow or add IP via Azure Portal
  ip_rules = []

  depends_on = [
    null_resource.enable_service_endpoint,
    azurerm_kubernetes_cluster.aks
  ]
}
