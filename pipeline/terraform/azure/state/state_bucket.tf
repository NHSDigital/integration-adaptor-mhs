variable state_bucket_rg {
  description = "Resource group which contains bucket with TF state file"
  default  = "nia-rg-tfstate"
}

variable state_bucket_storage_account {
  description = "Name of storage account with TF state bucket"
  default = "niafstate"
}

variable state_bucket_name {
  description = "Name of bucket (container) with state file"
  default = "nia-tf-state-container"
}

variable "base_state_bucket_file" {
  default = "base.tfstate"
}

variable mhs_state_bucket_file {
  description = "Name of file with TF state"
  default = "mhs.tfstate"
}

variable nhais_state_bucket_file {
  default = "nhais.tfstate"
}

variable gp2gp_state_bucket_file {
  default = "gp2gp.tfstate"
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
  resource_group_name = var.state_bucket_rg
  name = var.state_bucket_storage_account
  location = var.location
  account_tier = "Standard"
  account_replication_type = "LRS"

  depends_on = [ azurerm_resource_group.state_bucket_rg ]
}

resource "azurerm_storage_container" "state_bucket_container" {
  name = var.state_bucket_name
  storage_account_name = azurerm_storage_account.state_bucket_sa.name
}

output "tf_state_storage_account_name" {
  value = azurerm_storage_account.state_bucket_sa.name
}

output "tf_state_container_name" {
  value = azurerm_storage_container.state_bucket_container.name
}

output "tf_state_account_key" {
  value = azurerm_storage_account.state_bucket_sa.primary_access_key
}

output "tf_state_connection_string" {
  value = azurerm_storage_account.state_bucket_sa.primary_connection_string
}
