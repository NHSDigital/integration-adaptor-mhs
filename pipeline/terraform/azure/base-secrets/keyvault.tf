resource "azurerm_key_vault" "nia-base-key-vault" {
  name                = "nia-base-key-vault"
  #resource_group_name = azurerm_resource_group.nia_base.name
  #location            = azurerm_resource_group.nia_base.location
  resource_group_name = data.terraform_remote_state.base.outputs.resource_group_name
  location = data.terraform_remote_state.base.outputs.resource_group_location
  tenant_id           = data.azurerm_client_config.current.tenant_id
  soft_delete_enabled         = false
  #soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"

  network_acls {
    default_action = "Deny"
    bypass         = "AzureServices"
    ip_rules       = var.secret_jumpbox_allowed_ips
  }
}

resource "azurerm_key_vault_access_policy" "terraform" {
    key_vault_id = azurerm_key_vault.nia-base-key-vault.id
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    key_permissions = [
      "get",
      "create",
      "list",
      "update",
      "delete",
    ]

    secret_permissions = [
      "get",
      "set",
      "list",
      "delete",
    ]

    storage_permissions = [
      "get",
      "set",
      "list",
      "update",
      "delete",
    ]
}

resource "azurerm_key_vault_access_policy" "console" {
  key_vault_id = azurerm_key_vault.nia-base-key-vault.id
  tenant_id = var.console_tenant_id
  object_id = var.console_object_id

      key_permissions = [
      "get",
      "create",
      "list",
      "update",
      "delete",
    ]

    secret_permissions = [
      "get",
      "set",
      "list",
      "delete",
    ]

    storage_permissions = [
      "get",
      "set",
      "list",
      "update",
      "delete",
    ]
}

data "azurerm_client_config" "current" {}
