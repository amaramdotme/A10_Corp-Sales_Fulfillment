module "aks" {
  source = "../../modules/aks-cluster"

  cluster_name        = "aks-a10corp-sales-prod"
  resource_group_name = "rg-a10corp-sales-prod"
  location            = "eastus"
  dns_prefix          = "a10sales-prod"
  
  vnet_name           = "vnet-a10corp-sales-prod"
  subnet_name         = "snet-a10corp-sales-prod-aks-nodes"
  identity_name       = "id-a10corp-sales-prod"

  # Fixes for ACR access and NSG rules
  acr_id              = "/subscriptions/fdb297a9-2ece-469c-808d-a8227259f6e8/resourceGroups/rg-root-iac/providers/Microsoft.ContainerRegistry/registries/acra10corpsales"
  node_nsg_name       = "nsg-a10corp-sales-prod-aks-nodes"

  # Prod Specifics: High availability
  node_count          = 3
  vm_size             = "Standard_D2s_v3"

  tags = {
    Environment = "Prod"
    Workload    = "SalesFulfillment"
    ManagedBy   = "Terraform"
  }
}

module "sql" {
  source = "../../modules/azure-sql"

  server_name         = "sql-a10sales-prod-v2"
  database_name       = "db-sales-fulfillment"
  resource_group_name = "rg-a10corp-sales-prod"
  location            = "eastus2" 
  
  admin_username      = "sqladmin"
  admin_password      = "P@ssw0rdProd789!" # Note: Use variables/keyvault in production

  aks_subnet_id       = module.aks.node_subnet_id
  sku_name            = "S0" 

  # Cross-region fix
  enable_vnet_rule     = false
  allow_azure_services = true

  tags = {
    Environment = "Prod"
    Workload    = "SalesFulfillment"
    ManagedBy   = "Terraform"
  }
}