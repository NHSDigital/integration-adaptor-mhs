resource "azurerm_servicebus_namespace" "mhs_inbound_servicebus_namespace" {
  count               = var.use_servicebus ? 1 : 0
  name                = "${var.cluster_name}-servicebus"
  location            = azurerm_resource_group.mhs_adaptor.location
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  capacity            = 1
  sku                 = "Premium"
}

resource "azurerm_servicebus_queue" "mhs_inbound_queue" {
  count               = var.use_servicebus ? 1 : 0
  name                = "${var.cluster_name}-servicebus-inbound-queue"
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  namespace_name      = azurerm_servicebus_namespace.mhs_inbound_servicebus_namespace[0].name

  enable_partitioning = false
}

resource "azurerm_servicebus_namespace_authorization_rule" "mhs_servicebus_ar" {
  count               = var.use_servicebus ? 1 : 0
  name = "${var.cluster_name}-servicebus_ar"
  resource_group_name = azurerm_resource_group.mhs_adaptor.name
  namespace_name = azurerm_servicebus_namespace.mhs_inbound_servicebus_namespace[0].name

  listen = true
  send = true
  manage = false
}

output "inbound_service_bus_host" {
  description = "Hostname for Service Bus endpoint"
  value = var.use_servicebus ? replace(replace(split(";",azurerm_servicebus_namespace_authorization_rule.mhs_servicebus_ar[0].primary_connection_string)[0],"Endpoint=sb://",""),"/","") : "rabbitmq"
}

output "inbound_service_bus_port" {
  value = var.use_servicebus ? "5671" : "5672"
}

output "service_bus_protocol" {
  value = var.use_servicebus ? "amqps" : "amqp"
}

output "inbound_service_bus_queue_name" {
  value = var.use_servicebus ? azurerm_servicebus_queue.mhs_inbound_queue[0].name : "mhs-inbound"
}

output "inbound_service_bus_queue_username" {
   value = var.use_servicebus ? azurerm_servicebus_namespace_authorization_rule.mhs_servicebus_ar[0].name : "guest"
}

output "inbound_servicebus_ar_primary_key" {
  value = var.use_servicebus ? azurerm_servicebus_namespace_authorization_rule.mhs_servicebus_ar[0].primary_key : "guest"
}
