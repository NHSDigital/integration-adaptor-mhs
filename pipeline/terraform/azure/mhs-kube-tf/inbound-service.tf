# resource "kubernetes_service" "inbound" {
#   metadata {
#     name = "inbound"
#     # annotations = {
#     #   kompose.cmd = "kompose convert"
#     #   kompose.version = "1.21.0 ()"
#     # }
#     # labels = {
#     #   io.kompose.service = "inbound"
#     # }
#   }

#   spec {
#     port {
#       port = 443
#       target_port = 443
#     }

#     port {
#       port = 80
#       target_port = 80
#     }
    
#     # selector = {
#     #   io.kompose.service = "inbound"
#     # }
#   }
# }
