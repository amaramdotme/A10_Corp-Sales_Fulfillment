#!/bin/bash

# Configuration
APP_NAME="github-oidc-sales-fulfillment"
GH_ORG="amaramdotme"
GH_REPO="A10_Corp-Sales_Fulfillment"

echo "Setting up OIDC for $GH_ORG/$GH_REPO..."

# 1. Create the Azure AD Application
APP_ID=$(az ad app create --display-name "$APP_NAME" --query appId -o tsv)
echo "Created App ID: $APP_ID"

# 2. Create Service Principal
SP_ID=$(az ad sp create --id "$APP_ID" --query id -o tsv)
echo "Created Service Principal Object ID: $SP_ID"

# 3. Create Federated Identity Credentials for all environments
ENVIRONMENTS=("dev" "stage" "prod")

for ENV in "${ENVIRONMENTS[@]}"; do
    echo "Creating Federated Credential for environment: $ENV"
    az ad app federated-credential create --id "$APP_ID" --parameters "{
        \"name\": \"github-sales-${ENV}-env\",
        \"issuer\": \"https://token.actions.githubusercontent.com\",
        \"subject\": \"repo:$GH_ORG/$GH_REPO:environment:$ENV\",
        \"description\": \"OIDC for Sales Fulfillment $ENV Environment\",
        \"audiences\": [\"api://AzureADTokenExchange\"]
    }"
done

echo "--------------------------------------------------"
echo "OIDC Setup Complete!"
echo "App Name: $APP_NAME"
echo "Client ID (AZURE_CLIENT_ID): $APP_ID"
echo "Tenant ID (AZURE_TENANT_ID): $(az account show --query tenantId -o tsv)"
echo "--------------------------------------------------"
echo "Next Steps:"
echo "1. Assign RBAC roles manually for this SP ($APP_ID)."
echo "2. Add these values to your GitHub Secrets."
echo "--------------------------------------------------"
