module "aks" {
  source = "../../modules/aks-cluster"

  cluster_name        = "aks-a10corp-sales-stage"
  resource_group_name = "rg-a10corp-sales-stage"
  location            = "eastus"
  dns_prefix          = "a10sales-stage"
  
  vnet_name           = "vnet-a10corp-sales-stage"
  subnet_name         = "snet-a10corp-sales-stage-aks-nodes"
  identity_name       = "id-a10corp-sales-stage"

  node_count          = 2
  vm_size             = "Standard_B2s"

  tags = {
    Environment = "Stage"
    Workload    = "SalesFulfillment"
    ManagedBy   = "Terraform"
  }
}
