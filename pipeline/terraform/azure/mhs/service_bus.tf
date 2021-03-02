resource "azurerm_servicebus_namespace" "mhs_inbound_servicebus_namespace" {
  name                = "${var.cluster_name}-servicebus"
  location            = azurerm_resource_group.mhs_adaptor.location
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  capacity            = 1
  sku                 = "Premium"
}

resource "azurerm_servicebus_queue" "mhs_inbound_queue" {
  name                = "${var.cluster_name}-servicebus-inbound-queue"
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  namespace_name      = azurerm_servicebus_namespace.mhs_inbound_servicebus_namespace.name

  enable_partitioning = false
}

resource "azurerm_servicebus_namespace_authorization_rule" "mhs_servicebus_ar" {
  name = "${var.cluster_name}-servicebus_ar"
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  namespace_name = azurerm_servicebus_namespace.mhs_inbound_servicebus_namespace.name

  listen = true
  send = true
  manage = false
}

output "inbound_service_bus_host" {
  description = "Hostname for Service Bus endpoint"
  value = replace(replace(split(";",azurerm_servicebus_namespace_authorization_rule.mhs_servicebus_ar.primary_connection_string)[0],"Endpoint=sb://",""),"/","")
}


          # env {
          #   name = "NHAIS_AMQP_BROKERS"
          #   value = "amqps://${replace(replace(split(";", azurerm_servicebus_namespace_authorization_rule.nhais_servicebus_ar.primary_connection_string)[0],"Endpoint=sb://",""),"/","")}:5671/?sasl=plain"
          # }

  #           type = "Opaque"
  # data = {
  #   broker =  "amqps://${data.terraform_remote_state.mhs.outputs.inbound_service_bus_host}:${data.terraform_remote_state.mhs.outputs.inbound_service_bus_port}/?sasl=plain"
  #   queue = data.terraform_remote_state.mhs.outputs.inbound_service_bus_queue_name
  #   username = data.terraform_remote_state.mhs.outputs.inbound_service_bus_queue_username
  #   password = data.terraform_remote_state.mhs.outputs.inbound_service_bus_primary_key
  # }

output "inbound_service_bus_port" {
  value = "5671"
}

output "inbound_service_bus_queue_name" {
  value = azurerm_servicebus_queue.mhs_inbound_queue.name
}

output "inbound_service_bus_queue_username" {
   value = azurerm_servicebus_namespace_authorization_rule.mhs_servicebus_ar.name
}

output "inbound_service_bus_connection_string" {
  description = "Primary connection string for Service Bus Namespace"
  value = azurerm_servicebus_namespace_authorization_rule.mhs_servicebus_ar.primary_connection_string
}

output "inbound_servicebus_ar_primary_key" {
  value = azurerm_servicebus_namespace_authorization_rule.mhs_servicebus_ar.primary_key
}

