terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
    }
  }
}

provider "kubernetes" {
  load_config_file = false
  host = data.terraform_remote_state.mhs.outputs.host
  client_certificate = base64decode(data.terraform_remote_state.mhs.outputs.client_certificate)
  client_key = base64decode(data.terraform_remote_state.mhs.outputs.client_key)
  cluster_ca_certificate = base64decode(data.terraform_remote_state.mhs.outputs.cluster_ca_certificate)
}
