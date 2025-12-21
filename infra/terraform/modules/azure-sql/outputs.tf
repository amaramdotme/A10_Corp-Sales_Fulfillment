output "server_fqdn" {
  value = azurerm_mssql_server.sql.fully_qualified_domain_name
}

output "database_name" {
  value = azurerm_mssql_database.db.name
}

output "admin_username" {
  value = var.admin_username
}

output "admin_password" {
  value     = var.admin_password
  sensitive = true
}

output "connection_string_jdbc" {
  value     = "jdbc:sqlserver://${azurerm_mssql_server.sql.fully_qualified_domain_name}:1433;database=${azurerm_mssql_database.db.name};user=${var.admin_username}@${azurerm_mssql_server.sql.name};password=${var.admin_password};encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;"
  sensitive = true
}

output "connection_string_sqlalchemy" {
  value     = "mssql+pyodbc://${var.admin_username}:${var.admin_password}@${azurerm_mssql_server.sql.fully_qualified_domain_name}/${azurerm_mssql_database.db.name}?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection+Timeout=30"
  sensitive = true
}
