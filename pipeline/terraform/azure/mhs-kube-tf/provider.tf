terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
    }
  }
}

provider "kubernetes" {
  load_config_file = false
  host = replace(data.terraform_remote_state.mhs.outputs.host,"443", "8443")
  #username = data.terraform_remote_state.mhs.outputs.kube_config.username
  #password = data.terraform_remote_state.mhs.outputs.kube_config.password
  
  client_certificate = base64decode(data.terraform_remote_state.mhs.outputs.client_certificate)
  client_key = base64decode(data.terraform_remote_state.mhs.outputs.client_key)
  cluster_ca_certificate = base64decode(data.terraform_remote_state.mhs.outputs.cluster_ca_certificate)
}
