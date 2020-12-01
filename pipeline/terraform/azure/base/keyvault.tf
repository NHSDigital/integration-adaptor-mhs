resource "azurerm_key_vault" "nia-base-key-vault" {
  name                = "nia-base-key-vault"
  resource_group_name = azurerm_resource_group.nia_base.name
  location            = azurerm_resource_group.nia_base.location
  tenant_id           = data.azurerm_client_config.current.tenant_id
  soft_delete_enabled         = false
  #soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    key_permissions = [
      "get",
    ]

    secret_permissions = [
      "get",
    ]

    storage_permissions = [
      "get",
    ]
  }

  network_acls {
    default_action = "Deny"
    bypass         = "AzureServices"
  }


}

data "azurerm_client_config" "current" {}