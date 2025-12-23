# Next Steps

## CI/CD
- [x] **Implement `deploy-stage.yml` & `deploy-prod.yml`**:
    - Integrated into `sales_fulfillment-devops.yml`.
- [x] **Implement Direct Production Deployment strategy**:
    - Replaced Blue/Green with Direct Deployment in `sales_fulfillment-devops.yml`.
- [x] **Teardown on-demand**:
    - Implemented `teardown-on-demand.yml` for manual decommissioning.
- [x] **Consolidate On-Demand workflows**:
    - Merged `dev-on-demand.yml` into a parameterized `start-on-demand.yml` for all environments.
- [x] **Fix Prod Deployment**: Reduced node count for vCPU quota and resolved NSG conflicts.
- [x] **Fix SQLite Deadlock**: Implemented `Recreate` deployment strategy to handle RWO volume locking.

## Infrastructure
- [x] **Database Strategy**: Migrated from Azure SQL to SQLite with Azure Blob Storage backups.
- [x] **Storage Network Access**: Foundation team updated storage account to allow all traffic.
- [x] **Blob Backup Fix**: Resolved `AuthorizationPermissionMismatch` and `Multiple user assigned identities exist` by correcting storage account name and explicitly setting `AZURE_CLIENT_ID`.
- [x] **Observability**: Set up Azure Monitor and Log Analytics integration.

## Cost Management
- [x] **Automated Shutdown**: Implemented `shutdown-all-env.yml` to scale workloads to 0 in all environments when not in use.

## Observability Utilization
- [x] **Log Queries**: Created `docs/observability_queries.md` and saved KQL queries (prefixed with `a10_`) to the Log Analytics Workspace.
- [x] **Dashboards**: Created Chart/Visualization variants for key metrics (App Logs, Errors, Restarts, CPU/Memory) accessible via "Saved Searches".

## Security
- [ ] **Entra ID Integration**: Implement Azure AD authentication for the application.
