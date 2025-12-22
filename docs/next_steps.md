# Next Steps

## CI/CD
- [ ] **Implement `deploy-stage.yml` & `deploy-prod.yml`**: 
    - Create GitHub Action workflows for Stage and Prod environments.
    - Trigger on merge to `main` (Stage) and tagged releases (Prod).
- [x] **Refine `dev-on-demand.yml`**:
    - Added automatic provisioning and teardown of Azure SQL.
    - Integrated Terraform outputs with Helm deployment.

## Infrastructure
- [x] **Database Module**: Implemented Terraform module for Azure SQL with VNet security rules.
- [ ] **Observability**: Set up Azure Monitor and Log Analytics integration.

## Security
- [ ] **Entra ID Integration**: Implement Azure AD authentication for the application.
