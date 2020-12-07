# resource "kubernetes_config_map" "dns" {
#   metadata {
#     name = "coredns-custom"
#     namespace = var.mhs_namespace
#   }

#   data = {
#     nhs.server = "nhs.uk:53 {\n  errors\n  cache 30\n  log\n  forward . ${join(" ", data.terraform_remote_state.mhs.outputs.nhs_dns)}\n}\n"
#   }
# }

# To apply this: kubectl apply -f dns.yaml && kubectl -n kube-system rollout restart deployment coredns
