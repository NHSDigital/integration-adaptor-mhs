resource "kubernetes_secret" "mhs-partykey" {
  metadata {
    name = "mhs-partykey"
    namespace = var.mhs_namespace
  }
  type = "Opaque"
  data = {
    partyKey =  data.terraform_remote_state.base-secrets.outputs.nia-secret-mhs-partykey_value
  }
}

resource "kubernetes_secret" "mhs-queue" {
  metadata {
    name = "mhs-queue"
    namespace = var.mhs_namespace
  }
  type = "Opaque"
  data = {
    broker =  "amqps://${data.terraform_remote_state.mhs.outputs.inbound_service_bus_host}:${data.terraform_remote_state.mhs.outputs.inbound_service_bus_port}/?sasl=plain"
    queue = data.terraform_remote_state.mhs.outputs.inbound_service_bus_queue_name
    username = data.terraform_remote_state.mhs.outputs.inbound_service_bus_queue_username
    password = data.terraform_remote_state.mhs.outputs.inbound_service_bus_primary_key
  }
}

resource "kubernetes_secret" "mhs-database" {
  metadata {
    name = "mhs-database"
    namespace = var.mhs_namespace
  }
  type = "Opaque"
  data = {
    connectionString =  data.terraform_remote_state.mhs.outputs.mongodb_connection_string.0
  }
}

resource "kubernetes_secret" "mhs-client-cert" {
  metadata {
    name = "mhs-client-cert"
    namespace = var.mhs_namespace
  }
  type = "Opaque"
  data = {
    tlscrt = data.terraform_remote_state.base-secrets.outputs.nia-secret-mhs-client-certificate_value
    tlskey = data.terraform_remote_state.base-secrets.outputs.nia-secret-mhs-client-key_value
  }
}

resource "kubernetes_secret" "mhs-ca-certs" {
  metadata {
    name = "mhs-ca-certs"
    namespace = var.mhs_namespace
  }
  type = "Opaque"
  data = {
    ca-certs =  data.terraform_remote_state.base-secrets.outputs.nia-secret-mhs-ca-chain_value
  }
}
