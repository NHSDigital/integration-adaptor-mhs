terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
    }
  }
}

provider "kubernetes" {
  load_config_file = false
  host = data.remote_state.mhs.kube_config.0.host
  username = data.remote_state.mhs.kube_config.0.username
  password = data.remote_state.mhs.kube_config.0.password
  
  client_certificate = "${base64decode(data.remote_state.mhs.kube_config.0.client_certificate)}"
  client_key = "${base64decode(data.remote_state.mhs.kube_config.0.client_key)}"
  cluster_ca_certificate = "${base64decodedata.remote_state.mhs.kube_config.0.cluster_ca_certificate)}"
}