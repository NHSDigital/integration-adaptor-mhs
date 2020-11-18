## Azure resource group for the kubernetes cluster ##
resource "azurerm_resource_group" "nia_base" {
  name     = var.resource_group_name
  location = var.location
}