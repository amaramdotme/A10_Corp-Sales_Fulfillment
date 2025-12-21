output "aks_cluster_name" {
  value = module.aks.cluster_name
}

output "aks_cluster_id" {
  value = module.aks.cluster_id
}

output "node_resource_group" {
  value = module.aks.node_resource_group
}

output "database_url" {
  value     = module.sql.connection_string_sqlalchemy
  sensitive = true
}
