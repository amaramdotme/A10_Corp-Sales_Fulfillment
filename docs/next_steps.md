# Next Steps

## CI/CD
- [x] **Implement `deploy-stage.yml` & `deploy-prod.yml`**: 
    - Integrated into `sales_fulfillment-devops.yml`.
- [x] **Implement Blue/Green Production strategy**:
    - Managed via `deploy-prod-green` and `promote-to-prod.yml`.
- [x] **Teardown on-demand**:
    - Implemented `teardown-on-demand.yml` for manual decommissioning.

## Infrastructure
- [x] **Database Module**: Implemented Terraform module for Azure SQL with VNet security rules.
- [ ] **Infrastructure Refactoring**: Move VNET/Subnet ownership from Foundation to this repository.
- [ ] **Observability**: Set up Azure Monitor and Log Analytics integration.

## Security
- [ ] **Entra ID Integration**: Implement Azure AD authentication for the application.
