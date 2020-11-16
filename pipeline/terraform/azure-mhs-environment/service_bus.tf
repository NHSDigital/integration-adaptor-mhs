resource "azurerm_servicebus_namespace" "mhs_inbound_servicebus_namespace" {
  name                = "${var.cluster_name}-service-bus"
  location            = azurerm_resource_group.mhs_adaptor.location
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  sku                 = "Basic"
}

resource "azurerm_servicebus_queue" "mhs_inbound_queue" {
  name                = "${var.cluster_name}-servicebus-queue"
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  namespace_name      = azurerm_servicebus_namespace.mhs_inbound_servicebus_namespace.name

  enable_partitioning = true
}

resource "azurerm_servicebus_queue_authorization_rule" "mhs_inboud_queue_ar" {
  name = "${var.cluster_name}-servicebus-queue-ar"
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  namespace_name = azurerm_servicebus_namespace.mhs_inbound_servicebus_namespace.name
  queue_name = azurerm_servicebus_queue.mhs_inbound_queue.name

  listen = true
  send = true
  manage = false
}


output "inbound_service_bus_connection_string" {
  description = "Primary connection string for Service Bus Namespace"
  value = azurerm_servicebus_namespace.mhs_inbound_servicebus_namespace.default_primary_connection_string
}

output "inbound_service_bus_primary_key" {
  description = "Primary key for Service Bus Namespace"
  value = azurerm_servicebus_namespace.mhs_inbound_servicebus_namespace.default_primary_key
}

output "inbound_queue_ar_primary_key" {
  value = azurerm_servicebus_queue_authorization_rule.mhs_inboud_queue_ar.primary_key
}

output "inbound_queue_ar_primary_connection_string" {
  value = azurerm_servicebus_queue_authorization_rule.mhs_inboud_queue_ar.primary_connection_string
}
