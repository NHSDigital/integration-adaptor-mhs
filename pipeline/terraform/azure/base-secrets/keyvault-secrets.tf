resource "azurerm_key_vault_secret" "nia-secret-mhs-partykey" {
  name         = "nia-secret-mhs-partykey"
  value        = var.secret_mhs_partykey
  key_vault_id = azurerm_key_vault.nia-base-key-vault.id
  depends_on = [ azurerm_key_vault_access_policy.terraform ]
}

resource "azurerm_key_vault_secret" "nia-secret-mhs-ca-chain" {
  name = "nia-secret-mhs-ca-chain"
  value = var.secret_mhs_ca_chain
  key_vault_id = azurerm_key_vault.nia-base-key-vault.id
  depends_on = [ azurerm_key_vault_access_policy.terraform ]
}

resource "azurerm_key_vault_secret" "nia-secret-mhs-client-certificate" {
  name = "nia-secret-mhs-client-certificate"
  value = var.secret_mhs_client_certificate
  key_vault_id = azurerm_key_vault.nia-base-key-vault.id
  depends_on = [ azurerm_key_vault_access_policy.terraform ]
}

resource "azurerm_key_vault_secret" "nia-secret-mhs-client-key" {
  name = "nia-secret-mhs-client-key"
  value = var.secret_mhs_client_key
  key_vault_id = azurerm_key_vault.nia-base-key-vault.id
  depends_on = [ azurerm_key_vault_access_policy.terraform ]
}

resource "azurerm_key_vault_secret" "nia-secret-mhs-route-spine-ca-certs" {
  name = "nia-secret-mhs-route-spine-ca-certs"
  value = var.secret_mhs_spine_route_ca_certs
  key_vault_id = azurerm_key_vault.nia-base-key-vault.id
  depends_on = [ azurerm_key_vault_access_policy.terraform ]
}

output key_vault_id {
  value       = azurerm_key_vault.nia-base-key-vault.id
}

output nia-secret-mhs-partykey_name {
  value  = azurerm_key_vault_secret.nia-secret-mhs-partykey.name
}

output nia-secret-mhs-ca-chain_name {
  value  = azurerm_key_vault_secret.nia-secret-mhs-ca-chain.name
}

output nia-secret-mhs-client-certificate_name {
  value  = azurerm_key_vault_secret.nia-secret-mhs-client-certificate.name
}

output nia-secret-mhs-client-key_name {
  value  = azurerm_key_vault_secret.nia-secret-mhs-client-key.name
}

output nia-secret-mhs-route-spine-ca-certs_name {
  value = azurerm_key_vault_secret.nia-secret-mhs-route-spine-ca-certs.name
}

output nia-secret-mhs-route-spine-ca-certs_value {
  value = azurerm_key_vault_secret.nia-secret-mhs-route-spine-ca-certs.value
  sensitive = true
}

output nia-secret-mhs-partykey_value {
  value  = azurerm_key_vault_secret.nia-secret-mhs-partykey.value
  sensitive = true
}

output nia-secret-mhs-ca-chain_value {
  value  = azurerm_key_vault_secret.nia-secret-mhs-ca-chain.value
  sensitive = true
}

output nia-secret-mhs-client-certificate_value {
  value  = azurerm_key_vault_secret.nia-secret-mhs-client-certificate.value
  sensitive = true
}

output nia-secret-mhs-client-key_value {
  value  = azurerm_key_vault_secret.nia-secret-mhs-client-key.value
  sensitive = true
}
