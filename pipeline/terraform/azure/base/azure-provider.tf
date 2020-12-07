## Azure resource provider ##
terraform {
  required_version = ">= 0.12"

  backend "azurerm" {
    resource_group_name  = "nia-rg-tfstate"
    storage_account_name = "niafstate"
    container_name       = "nia-tf-state-container"
    key                  = "base.tfstate"
  }
}

provider "azurerm" {
  version = "~>2.5"
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }
}
