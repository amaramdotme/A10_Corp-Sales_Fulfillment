module "aks" {
  source = "../../modules/aks-cluster"

  cluster_name        = "aks-a10corp-sales-dev"
  resource_group_name = "rg-a10corp-sales-dev"
  location            = "eastus"
  dns_prefix          = "a10sales-dev"
  
  vnet_name           = "vnet-a10corp-sales-dev"
  subnet_name         = "snet-a10corp-sales-dev-aks-nodes"
  identity_name       = "id-a10corp-sales-dev"

  # Dev Specifics: Lower node count, Cost optimized
  node_count          = 1
  vm_size             = "Standard_B2s"
  
  # Future optimization: Add spot instance support to module
  # enable_spot_instances = true 

  tags = {
    Environment = "Dev"
    Workload    = "SalesFulfillment"
    ManagedBy   = "Terraform"
  }
}
