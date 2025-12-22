terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  backend "azurerm" {
    # Configuration provided via -backend-config or environment variables
  }
}

provider "azurerm" {
  features {}
  subscription_id = "385c6fcb-c70b-4aed-b745-76bd608303d7" # sub-sales
}
