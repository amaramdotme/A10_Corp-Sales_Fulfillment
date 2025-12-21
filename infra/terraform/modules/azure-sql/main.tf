resource "azurerm_mssql_server" "sql" {
  name                         = var.server_name
  resource_group_name          = var.resource_group_name
  location                     = var.location
  version                      = "12.0"
  administrator_login          = var.admin_username
  administrator_login_password = var.admin_password

  tags = var.tags
}

resource "azurerm_mssql_database" "db" {
  name           = var.database_name
  server_id      = azurerm_mssql_server.sql.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  sku_name       = var.sku_name
  max_size_gb    = 2

  tags = var.tags
}

# Allow access from AKS Subnet (only if in same region)
resource "azurerm_mssql_virtual_network_rule" "aks" {
  count     = var.enable_vnet_rule ? 1 : 0
  name      = "allow-aks-subnet"
  server_id = azurerm_mssql_server.sql.id
  subnet_id = var.aks_subnet_id
}

# Allow all Azure Services (required if SQL and AKS are in different regions)
resource "azurerm_mssql_firewall_rule" "allow_azure_services" {
  count            = var.allow_azure_services ? 1 : 0
  name             = "AllowAzureServices"
  server_id        = azurerm_mssql_server.sql.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

# Optional: Allow access from a specific public IP
resource "azurerm_mssql_firewall_rule" "public" {
  count            = var.allow_public_access && var.public_ip != null ? 1 : 0
  name             = "AllowPublicIP"
  server_id        = azurerm_mssql_server.sql.id
  start_ip_address = var.public_ip
  end_ip_address   = var.public_ip
}
