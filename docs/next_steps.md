# Next Steps

## CI/CD
- [ ] **Implement `deploy-dev.yml`**: 
    - Create a GitHub Action workflow to deploy to the Azure Dev environment (`rg-a10corp-sales-dev`).
    - Trigger on merge to `main`.
    - Steps:
        - Log in to Azure (OIDC).
        - Terraform Apply (ensure AKS cluster exists).
        - Build and Push Docker images to ACR.
        - Helm Upgrade/Install to AKS.
    - **Cost Optimization**: Ensure the Terraform configuration for this environment uses Spot instances and enables the cluster autoscaler. Consider adding a nightly shutdown workflow.

## Infrastructure
- [ ] **Database Module**: Implement Terraform module for Azure SQL or CosmosDB.
- [ ] **Observability**: Set up Azure Monitor and Log Analytics integration.

## Security
- [ ] **Entra ID Integration**: Implement Azure AD authentication for the application.
