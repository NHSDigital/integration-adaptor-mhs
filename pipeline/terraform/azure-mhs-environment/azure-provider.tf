## Azure resource provider ##
terraform {
  required_version = ">= 0.12"
}

provider "azurerm" {
  version = "~>2.5"
  features {}
}