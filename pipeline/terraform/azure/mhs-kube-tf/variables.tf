variable state_bucket_storage_account {
  description = "Name of storage account with TF state bucket"
  default = "niafstate"
}

variable state_bucket_name {
  description = "Name of bucket (container) with state file"
  default = "nia-tf-state-container"
}

variable "mhs_namespace" {
  default = "default"
}

variable "persistence_adaptor" {
  default = "mongodb"
}

variable "inbound_use_ssl" {
  default = false
}

variable "inbound_queue_message_ttl_in_seconds" {
  default = 0
}

variable "service_ports" {
  default = "443,80"
}

variable "tcp_ports" {
  default = "80"
}