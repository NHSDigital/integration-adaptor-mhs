variable state_bucket_rg {
  description = "Resource group which contains bucket with TF state file"
  default  = "mhs-rg-state"
}

variable state_bucket_storage_account {
  description = "Name of storage account with TF state bucket"
  default = "mhs-tfstate-sa"
}

variable state_bucket_name {
  description = "Name of bucket (container) with state file"
  default = "mhs-tf-state"
}

variable state_bucket_file {
  description = "Name of file with TF state"
  default = "mhs.tfstate"
}

variable location {
  default = "UK West"
}

terraform {
  required_version = ">= 0.12"
}

provider "azurerm" {
  version = "~>2.5"
  features {}
}

resource "azurerm_resource_group" "state_bucket_rg" {
  name     = var.state_bucket_rg
  location = var.location
}

resource "azurerm_storage_account" "state_bucket_sa" {
  name = var.state_bucket_storage_account
  location = var.location
  account_tier = "Standard"
  account_replication_type = "LRS"
}
