# resource "kubernetes_deployment" "inbound" {
#   metadata {
#     name = "inbound"
#     # labels = {
#     #   io.kompose.service = "inbound"
#     # }
#     # annotations = {
#     #   kompose.cmd = "kompose.convert"
#     #   kompose.version = "1.21.0 ()"
#     # }
#   }
#   spec {
#     replicas = 1
#     # selector {
#     #   match_labels = {
#     #     io.kompose.service: "inbound"
#     #   }
#     # }

#     template {
#       metadata {
#         # labels = {
#         #   io.kompose.service = "inbound"
#         # }
#         # annotations = {
#         #   kompose.cmd = "kompose.convert"
#         #   kompose.version = "1.21.0 ()"
#         # }
#       }

#       spec {
#         dns_policy=  "ClusterFirst"
#         restart_policy = "Always"
#         container {
#           image =  "nhsdev/nia-mhs-inbound:1.0.1"
#           name =  "inbound"
#           env {
#             name = "MHS_INBOUND_QUEUE_BROKERS"
#             value_from {
#               secret_key_ref {
#                 name = kubernetes_secret.mhs-queue.metadata[0].name
#                 key = "broker"
#               }
#             }
#           }
#           env {
#             name = "MHS_INBOUND_QUEUE_NAME"
#             value_from {
#               secret_key_ref {
#                 name = kubernetes_secret.mhs-queue.metadata[0].name
#                 key = "queue"
#               }
#             }
#           }
#           env {
#             name = "MHS_SECRET_INBOUND_QUEUE_USERNAME"
#             value_from {
#               secret_key_ref {
#                 name = kubernetes_secret.mhs-queue.metadata[0].name
#                 key = "username"
#               }
#             }
#           }
#           env {
#             name = "MHS_SECRET_INBOUND_QUEUE_PASSWORD"
#             value_from {
#               secret_key_ref {
#                 name = kubernetes_secret.mhs-queue.metadata[0].name
#                 key = "username"
#               }
#             }
#           }
#           env {
#             name = "MHS_SECRET_PARTY_KEY"
#             value_from {
#               secret_key_ref {
#                 name = kubernetes_secret.mhs-partykey.metadata[0].name
#                 key = "partyKey"
#               }
#             }
#           }
#           env {
#             name = "MHS_SECRET_CLIENT_CERT"
#             value_from {
#               secret_key_ref {
#                 name = kubernetes_secret.mhs-client-cert.metadata[0].name
#                 key = "tls.crt"
#               }
#             }
#           }
#           env {
#             name = "MHS_SECRET_CLIENT_KEY"
#             value_from {
#               secret_key_ref {
#                 name = kubernetes_secret.mhs-client-cert.metadata[0].name
#                 key = "tls.key"
#               }
#             }
#           }
#           env {
#             name =  "MHS_SECRET_CA_CERTS"
#             value_from {
#               secret_key_ref {
#                 name = kubernetes_secret.mhs-ca-certs.metadata[0].name
#                 key = "ca-certs"
#               }
#             }
#           }
#           env {
#             name = "MHS_DB_ENDPOINT_URL"
#             value = data.terraform_remote_state.mhs.outputs.db_endpoint
#           }
#           env {
#             name = "MHS_PERSISTENCE_ADAPTOR"
#             value = var.persistence_adaptor
#           }
#           env {
#             name = "MHS_INBOUND_USE_SSL"
#             value = var.inbound_use_ssl
#           }
#           env {
#             name = "MHS_INBOUND_QUEUE_MESSAGE_TTL_IN_SECONDS"
#             value = var.inbound_queue_message_ttl_in_seconds
#           }
#           env {
#             name = "MHS_LOG_LEVEL"
#             value = data.terraform_remote_state.mhs.outputs.mhs_log_level
#           }
#           env {
#             name = "MHS_STATE_TABLE_NAME"
#             value = data.terraform_remote_state.mhs.outputs.mhs_state_table_name
#           }
#           env {
#             name = "MHS_SYNC_ASYNC_STATE_TABLE_NAME"
#             value = data.terraform_remote_state.mhs.outputs.mhs_sync_async_table_name
#           }
#           env {
#             name = "SERVICE_PORTS"
#             value = var.service_ports
#           }
#           env {
#             name = "TCP_PORTS"
#             value = var.tcp_ports
#           }
#           port {
#             container_port = "443"
#           }
#           port {
#             container_port = "80"
#           }
#         }
#       }
#     }
#   }
# }
