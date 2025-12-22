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

## Infrastructure
- [x] **Database Strategy**: Migrated from Azure SQL to SQLite with Azure Blob Storage backups.
- [x] **Storage Network Access**: Foundation team updated storage account to allow all traffic (matches Terraform state storage configuration).
- [x] **Observability**: Set up Azure Monitor and Log Analytics integration.

## Cost Management
- [x] **Automated Shutdown**: Implemented `shutdown-all-env.yml` to scale workloads to 0 in all environments when not in use.

## Security
- [ ] **Entra ID Integration**: Implement Azure AD authentication for the application.
