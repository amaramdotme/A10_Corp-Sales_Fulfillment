module "aks" {
  source = "../../modules/aks-cluster"

  cluster_name        = "aks-a10corp-sales-prod"
  resource_group_name = "rg-a10corp-sales-prod"
  location            = "eastus"
  dns_prefix          = "a10sales-prod"
  
  vnet_name           = "vnet-a10corp-sales-prod"
  subnet_name         = "snet-a10corp-sales-prod-aks-nodes"
  identity_name       = "id-a10corp-sales-prod"

  # Infrastructure Access
  acr_id                     = "/subscriptions/fdb297a9-2ece-469c-808d-a8227259f6e8/resourceGroups/rg-root-iac/providers/Microsoft.ContainerRegistry/registries/acra10corpsales"
  storage_account_id         = "/subscriptions/fdb297a9-2ece-469c-808d-a8227259f6e8/resourceGroups/rg-root-iac/providers/Microsoft.Storage/storageAccounts/sta10corpsales"
  log_analytics_workspace_id = "/subscriptions/fdb297a9-2ece-469c-808d-a8227259f6e8/resourceGroups/rg-root-iac/providers/Microsoft.OperationalInsights/workspaces/log-a10corp-hq"
  node_nsg_name              = "nsg-a10corp-sales-prod-aks-nodes"

  # Prod Specifics: High availability
  node_count          = 3
  vm_size             = "Standard_D2s_v3"

  tags = {
    Environment = "Prod"
    Workload    = "SalesFulfillment"
    ManagedBy   = "Terraform"
  }
}