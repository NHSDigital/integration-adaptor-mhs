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




/*
#!/bin/bash
RESOURCE_GROUP_NAME=mhs-rg-state
STORAGE_ACCOUNT_NAME=mhs-tfstate-sa
CONTAINER_NAME=mhs-tf-state
LOCATION=ukwest

# Create resource group just for the bucket
az group create --name $RESOURCE_GROUP_NAME --location $LOCATION

# Create storage account
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS --encryption-services blob

# Get storage account key
STORAGE_ACCOUNT_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP_NAME --account-name $STORAGE_ACCOUNT_NAME --query '[0].value' -o tsv)

# Create blob container
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME --account-key $STORAGE_ACCOUNT_KEY

echo "storage_account_name: $STORAGE_ACCOUNT_NAME"
echo "container_name: $CONTAINER_NAME"
echo "access_key: $ACCOUNT_KEY"





*/