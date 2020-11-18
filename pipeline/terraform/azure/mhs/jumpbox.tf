resource "azurerm_public_ip" "mhs_jumpbox_pip" {
  name                = "mhs_jumpbox_pip"
  resource_group_name             = azurerm_resource_group.mhs_adaptor.name
  location                        = azurerm_resource_group.mhs_adaptor.location
  allocation_method   = "Dynamic"
}

resource "azurerm_network_security_group" "jumpbox_sg" {
  name                = "jumpbox_sg"
  resource_group_name             = azurerm_resource_group.mhs_adaptor.name
  location                        = azurerm_resource_group.mhs_adaptor.location
}

resource "azurerm_network_security_rule" "SSH" {
    name                        = "SSH"
    priority                    = 1001
    direction                   = "Inbound"
    access                      = "Allow"
    protocol                    = "Tcp"
    source_port_range           = "*"
    destination_port_range      = "22"
    source_address_prefixes     = var.jumpbox_allowed_ips
    destination_address_prefix  = "*"
    resource_group_name         = azurerm_resource_group.mhs_adaptor.name
    network_security_group_name = azurerm_network_security_group.jumpbox_sg.name
}

resource "azurerm_network_interface" "jumpbox_nic" {
  name                = "jumpbox-nic"
  resource_group_name             = azurerm_resource_group.mhs_adaptor.name
  location                        = azurerm_resource_group.mhs_adaptor.location

  ip_configuration {
    name                          = "vmNicConfiguration"
    subnet_id                     = azurerm_subnet.mhs_jumpbox_subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.mhs_jumpbox_pip.id
  }
}

resource "azurerm_network_interface_security_group_association" "sg_association" {
  network_interface_id      = azurerm_network_interface.jumpbox_nic.id
  network_security_group_id = azurerm_network_security_group.jumpbox_sg.id
}


resource "azurerm_linux_virtual_machine" "mhs_jumpbox" {
  name                            = "mhs_jumpbox"
  resource_group_name             = azurerm_resource_group.mhs_adaptor.name
  location                        = azurerm_resource_group.mhs_adaptor.location
  network_interface_ids           = [azurerm_network_interface.jumpbox_nic.id]
  size                            = "Standard_DS1_v2"
  computer_name                   = "jumpboxvm"
  admin_username                  = var.jumpbox_user
  admin_password                  = random_password.adminpassword.result
  disable_password_authentication = false

  admin_ssh_key {
    username = var.jumpbox_user
    public_key = file("../files/admin_ssh_key.pub")
  }

  os_disk {
    name                 = "jumpboxOsDisk"
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}

resource "random_password" "adminpassword" {
  keepers = {
    resource_group = azurerm_resource_group.mhs_adaptor.name
  }

  length      = 10
  min_lower   = 1
  min_upper   = 1
  min_numeric = 1
}

output "jumpbox_password" {
  description = "Jumpbox VM admin password"
  value       = random_password.adminpassword.result
}

output "jumpbox_ip" {
  description = "Jumpbox VM IP"
  value       = azurerm_linux_virtual_machine.mhs_jumpbox.public_ip_address
}

output "jumpbox_username" {
  description = "Jumpbox VM username"
  value       = var.jumpbox_user
}

output "jumpbox_connect" {
  description = "Command for connecting to jumpbox"
  value = "ssh ${var.jumpbox_user}@${azurerm_linux_virtual_machine.mhs_jumpbox.public_ip_address} -i ~/.ssh/azure_mhs_jumpbox"
}