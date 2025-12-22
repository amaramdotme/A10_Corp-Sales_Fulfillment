# Next Steps

## CI/CD
- [x] **Implement `deploy-stage.yml` & `deploy-prod.yml`**:
    - Integrated into `sales_fulfillment-devops.yml`.
- [x] **Implement Blue/Green Production strategy**:
    - Managed via `deploy-prod-green` and `promote-to-prod.yml`.
- [x] **Teardown on-demand**:
    - Implemented `teardown-on-demand.yml` for manual decommissioning.
- [x] **Fix Dev On-Demand workflow**:
    - Added missing Terraform Apply step.
- [x] **Fix Prod Deployment**: Reduced node count for vCPU quota and resolved NSG conflicts.

## Infrastructure
- [x] **Database Strategy**: Migrated from Azure SQL to SQLite with Azure Blob Storage backups.
- [x] **Storage Network Access**: Foundation team updated storage account to allow all traffic.
- [x] **Blob Backup Fix**: Resolved `AuthorizationPermissionMismatch` by correcting storage account name in workflows.
- [x] **Observability**: Set up Azure Monitor and Log Analytics integration.

## Cost Management
- [x] **Automated Shutdown**: Implemented `shutdown-all-env.yml` to scale workloads to 0 in all environments when not in use.

## Observability Utilization
- [ ] **Log Queries**: Create KQL queries to monitor application logs.
- [ ] **Dashboards**: Set up basic Azure Monitor dashboards for cluster health.

## Security
- [ ] **Entra ID Integration**: Implement Azure AD authentication for the application.
