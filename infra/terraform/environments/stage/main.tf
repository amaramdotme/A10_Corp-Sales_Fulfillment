module "aks" {
  source = "../../modules/aks-cluster"

  cluster_name        = "aks-a10corp-sales-stage"
  resource_group_name = "rg-a10corp-sales-stage"
  location            = "eastus"
  dns_prefix          = "a10sales-stage"
  
  vnet_name           = "vnet-a10corp-sales-stage"
  subnet_name         = "snet-a10corp-sales-stage-aks-nodes"
  identity_name       = "id-a10corp-sales-stage"

  # Infrastructure Access
  acr_id              = "/subscriptions/fdb297a9-2ece-469c-808d-a8227259f6e8/resourceGroups/rg-root-iac/providers/Microsoft.ContainerRegistry/registries/acra10corpsales"
  storage_account_id  = "/subscriptions/fdb297a9-2ece-469c-808d-a8227259f6e8/resourceGroups/rg-root-iac/providers/Microsoft.Storage/storageAccounts/sta10corpsales"
  node_nsg_name       = "nsg-a10corp-sales-stage-aks-nodes"

  node_count          = 2
  vm_size             = "Standard_D2s_v3"

  tags = {
    Environment = "Stage"
    Workload    = "SalesFulfillment"
    ManagedBy   = "Terraform"
  }
}