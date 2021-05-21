variable state_bucket_storage_account {
  description = "Name of storage account with TF state bucket"
  default = "niafstate"
}

variable state_bucket_name {
  description = "Name of bucket (container) with state file"
  default = "nia-tf-state-container"
}

##

variable "secret_mhs_partykey" {
  type = string
  default = "default_partykey"
}

variable "secret_mhs_ca_chain" {
  type = string
  default = "default_ca_chain"
}

variable "secret_mhs_client_certificate" {
  type = string
  default = "defualt_client_cert"
}

variable "secret_mhs_client_key" {
  type = string
  default = "default_client_key"
}

variable secret_mhs_spine_route_ca_certs {
  type = string
  default = "default_route_ca_certs"
}

variable "secret_jumpbox_allowed_ips" {
  description = "List of IPs that should be allowed to jumpbox, this value is not stored in Azure Keyvault and should always be loaded from tfvars"
  default = []
}

variable console_object_id {
  type = string
}

variable console_tenant_id {
  type = string
}
