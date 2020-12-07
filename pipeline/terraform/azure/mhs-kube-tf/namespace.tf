resource "kubernetes_namespace" "mhs" {
  metadata {
    name = var.mhs_namespace
  }
}