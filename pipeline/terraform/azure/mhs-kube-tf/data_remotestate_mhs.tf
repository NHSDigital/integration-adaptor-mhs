data "terraform_remote_state" "mhs" {
  backend = "azurerm"
  
  config = {
    storage_account_name = var.state_bucket_storage_account
    container_name = var.state_bucket_name
    key = "mhs.tfstate"
  }
}