resource "azurerm_public_ip" "mhs_firewall_pip" {
  name = "mhs_firewall_pip"
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  location            = azurerm_resource_group.mhs_adaptor.location
  allocation_method = "Static"
  sku = "Standard"
}

resource "azurerm_firewall" "mhs_firewall" {
  name = "mhs_firewall"
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  location            = azurerm_resource_group.mhs_adaptor.location

  ip_configuration {
    name = "mhs_fw_ip_config"
    subnet_id = azurerm_subnet.mhs_firewall_subnet.id
    public_ip_address_id = azurerm_public_ip.mhs_firewall_pip.id
  }
}

resource "azurerm_firewall_application_rule_collection" "mhs_aks_rules" {
  name = "mhs_aks_fw_rules"
  azure_firewall_name = azurerm_firewall.mhs_firewall.name
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  priority = "101"
  action = "Allow"

  rule {
    name = "allow network"
    source_addresses = ["*"]

    target_fqdns = [
      "*.cdn.mscr.io",
      "mcr.microsoft.com",
      "*.data.mcr.microsoft.com",
      "management.azure.com",
      "login.microsoftonline.com",
      "acs-mirror.azureedge.net",
      "dc.services.visualstudio.com",
      "*.opinsights.azure.com",
      "*.oms.opinsights.azure.com",
      "*.microsoftonline.com",
      "*.monitoring.azure.com",
      "*.azmk8s.io",
    ]

    protocol {
      port = "80"
      type = "Http"
    }

    protocol {
      port = "443"
      type = "Https"
    }
  }
}

resource "azurerm_firewall_network_rule_collection" "ntp" {
  name                = "time"
  azure_firewall_name = azurerm_firewall.mhs_firewall.name
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  priority            = 101
  action              = "Allow"

  rule {
    description           = "aks node time sync rule"
    name                  = "allow network"
    source_addresses      = ["*"]
    destination_ports     = ["123"]
    destination_addresses = ["*"]
    protocols             = ["UDP"]
  }
}

resource "azurerm_firewall_network_rule_collection" "dns" {
  name                = "dns"
  azure_firewall_name = azurerm_firewall.mhs_firewall.name
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  priority            = 102
  action              = "Allow"

  rule {
    description           = "aks node dns rule"
    name                  = "allow network"
    source_addresses      = ["*"]
    destination_ports     = ["53"]
    destination_addresses = ["*"]
    protocols             = ["UDP", "TCP"]
  }
}

resource "azurerm_firewall_network_rule_collection" "servicetags" {
  name                = "servicetags"
  azure_firewall_name = azurerm_firewall.mhs_firewall.name
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  priority            = 110
  action              = "Allow"

  rule {
    description       = "allow service tags"
    name              = "allow service tags"
    source_addresses  = ["*"]
    destination_ports = ["*"]
    protocols         = ["Any"]

    destination_addresses = [
      "AzureContainerRegistry",
      "MicrosoftContainerRegistry",
      "AzureActiveDirectory"
    ]
  }
}

resource "azurerm_firewall_application_rule_collection" "osupdates" {
  name                = "osupdates"
  azure_firewall_name = azurerm_firewall.mhs_firewall.name
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  priority            = 102
  action              = "Allow"

  rule {
    name             = "allow network"
    source_addresses = ["*"]

    target_fqdns = [
      "download.opensuse.org",
      "security.ubuntu.com",
      "ntp.ubuntu.com",
      "packages.microsoft.com",
      "snapcraft.io",
      "azure.archive.ubuntu.com",
      "deb.debian.org",
      "security.debian.org"
    ]

    protocol {
      port = "80"
      type = "Http"
    }

    protocol {
      port = "443"
      type = "Https"
    }
  }
}

resource "azurerm_firewall_application_rule_collection" "publicimages" {
  name                = "publicimages"
  azure_firewall_name = azurerm_firewall.mhs_firewall.name
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  priority            = 103
  action              = "Allow"

  rule {
    name             = "allow network"
    source_addresses = ["*"]

    target_fqdns = [
      "auth.docker.io",
      "registry-1.docker.io",
      "production.cloudflare.docker.com"
    ]

    protocol {
      port = "80"
      type = "Http"
    }

    protocol {
      port = "443"
      type = "Https"
    }
  }
}