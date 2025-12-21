module "aks" {
  source = "../../modules/aks-cluster"

  cluster_name        = "aks-a10corp-sales-dev"
  resource_group_name = "rg-a10corp-sales-dev"
  location            = "eastus"
  dns_prefix          = "a10sales-dev"
  
  vnet_name           = "vnet-a10corp-sales-dev"
  subnet_name         = "snet-a10corp-sales-dev-aks-nodes"
  identity_name       = "id-a10corp-sales-dev"
  
  # New fixes for ACR access and NSG rules
  acr_id              = "/subscriptions/fdb297a9-2ece-469c-808d-a8227259f6e8/resourceGroups/rg-root-iac/providers/Microsoft.ContainerRegistry/registries/acra10corpsales"
  node_nsg_name       = "nsg-a10corp-sales-dev-aks-nodes"

  # Dev Specifics: Lower node count, Cost optimized
  node_count          = 1
  vm_size             = "Standard_D2s_v3"
  
  # Future optimization: Add spot instance support to module
  # enable_spot_instances = true 

  tags = {
    Environment = "Dev"
    Workload    = "SalesFulfillment"
    ManagedBy   = "Terraform"
  }
}
