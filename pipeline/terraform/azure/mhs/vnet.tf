resource "azurerm_virtual_network" "mhs_vnet" {
  name                = "mhs_vnet"
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  location            = azurerm_resource_group.mhs_adaptor.location
  address_space       = [var.mhs_vnet_cidr]

  tags = {
    environment = "Production"
  }
}
