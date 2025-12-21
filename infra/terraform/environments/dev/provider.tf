terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  backend "azurerm" {
    # Configuration to be provided via -backend-config or environment variables
    # Expected: resource_group_name, storage_account_name, container_name, key
  }
}

provider "azurerm" {
  features {}
  # subscription_id is picked up from ARM_SUBSCRIPTION_ID env var
}
