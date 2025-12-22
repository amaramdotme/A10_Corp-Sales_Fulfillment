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
- [x] **Storage Network Access**: Configured Azure Service Endpoints for AKS-to-Blob connectivity.
- [ ] **Fix Storage Network Rules Terraform Conflict**:
    - Terraform trying to create `azurerm_storage_account_network_rules` but resource already exists
    - Options to discuss: Import existing rules, use `null_resource` with CLI, or manage differently
    - Affects both dev and stage deployments
- [ ] **Infrastructure Refactoring**: Move storage network rules and service endpoints to Foundation repo.
- [ ] **Observability**: Set up Azure Monitor and Log Analytics integration.

## Security
- [ ] **Entra ID Integration**: Implement Azure AD authentication for the application.
