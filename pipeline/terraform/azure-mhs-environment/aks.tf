
# Public IP for AKS cluster
# resource "azurerm_public_ip" "example" {
#   name                = "${var.cluster_name}_public_ip"
#   resource_group_name = azurerm_resource_group.mhs_adaptor.name
#   location            = azurerm_resource_group.mhs_adaptor.location
#   allocation_method   = "Static"

#   tags = {
#     environment = "Production"
#   }
# }

# MongoDB on CosmosDB

resource "azurerm_cosmosdb_account" "mongodb" {
  name = "${var.cluster_name}-mongodb"
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  location            = azurerm_resource_group.mhs_adaptor.location
  offer_type = "Standard"
  kind = "MongoDB"

  enable_automatic_failover = false

  capabilities {
    name = "MongoDBv3.4"
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 10
    max_staleness_prefix    = 200
  }

  geo_location {
    location          = azurerm_resource_group.mhs_adaptor.location
    failover_priority = 0
  }
}

output "mongodb_endpoint" {
  value = azurerm_cosmosdb_account.mongodb.endpoint
}

output "mongodb_write_endpoints" {
  value = azurerm_cosmosdb_account.mongodb.write_endpoints
}

output "mongodb_read_endpoints" {
  value = azurerm_cosmosdb_account.mongodb.read_endpoints
}

output "mongodb_connection_string" {
  value = azurerm_cosmosdb_account.mongodb.connection_strings
}

## AKS kubernetes cluster ##
resource "azurerm_kubernetes_cluster" "mhs_adaptor_exemplar" { 
  name                = var.cluster_name
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  location            = azurerm_resource_group.mhs_adaptor.location
  dns_prefix          = var.dns_prefix

  linux_profile {
    admin_username = var.admin_username

    ## SSH key is generated using "tls_private_key" resource
    ssh_key {
      key_data = "${trimspace(tls_private_key.key.public_key_openssh)} ${var.admin_username}@azure.com"
    }
  }

  addon_profile {
    http_application_routing {
      enabled = true
    }
  }

  agent_pool_profile {
    name            = "default"
    count           = var.agent_count
    vm_size         = "Standard_F2s_v2"
    os_type         = "Linux"
    os_disk_size_gb = 30
  }

  service_principal {
    client_id     = var.client_id
    client_secret = var.client_secret
  }

  tags = {
    Environment = "Production"
  }
}

## Private key for the kubernetes cluster ##
resource "tls_private_key" "key" {
  algorithm   = "RSA"
}

## Save the private key in the local workspace ##
resource "null_resource" "save-key" {
  triggers = {
    key = tls_private_key.key.private_key_pem
  }

  provisioner "local-exec" {
    command = <<EOF
      mkdir -p ${path.module}/.ssh
      echo "${tls_private_key.key.private_key_pem}" > ${path.module}/.ssh/id_rsa
      chmod 0600 ${path.module}/.ssh/id_rsa
EOF
  }
}

## Outputs ##

# Example attributes available for output
output "id" {
    value = "${azurerm_kubernetes_cluster.mhs_adaptor_exemplar.id}"
}

output "client_key" {
  value = "${azurerm_kubernetes_cluster.mhs_adaptor_exemplar.kube_config.0.client_key}"
}

output "client_certificate" {
  value = "${azurerm_kubernetes_cluster.mhs_adaptor_exemplar.kube_config.0.client_certificate}"
}

output "cluster_ca_certificate" {
  value = "${azurerm_kubernetes_cluster.mhs_adaptor_exemplar.kube_config.0.cluster_ca_certificate}"
}

output "kube_config" {
  value = azurerm_kubernetes_cluster.mhs_adaptor_exemplar.kube_config_raw
}

output "host" {
  value = azurerm_kubernetes_cluster.mhs_adaptor_exemplar.kube_config.0.host
}

output "configure" {
  value = <<CONFIGURE

Run the following commands to configure kubernetes client:

$ terraform output kube_config > ~/.kube/aksconfig
$ export KUBECONFIG=~/.kube/aksconfig

Test configuration using kubectl

$ kubectl get nodes
CONFIGURE
}