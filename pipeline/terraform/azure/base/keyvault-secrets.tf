resource "azurerm_key_vault_secret" "nia-secret-mhs-partykey" {
  name         = "nia-secret-mhs-partykey"
  value        = var.secret_mhs_partykey
  key_vault_id = azurerm_key_vault.nia-base-key-vault.id
}