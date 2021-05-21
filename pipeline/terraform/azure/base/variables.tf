## Azure config variables ##
variable "client_id" {}

variable "client_secret" {}

variable location {
  default = "UK West"
}

## Resource group variables ##
variable resource_group_name {
  default = "nia-base-rg"
}

variable jumpbox_user {
  default = "mhs_user"
}

variable "nia_vnet_cidr" {
  default = "10.20.0.0/16"
}

variable "jumpbox_subnet_cidr" {
  default = "10.20.1.0/24"
}

variable "secret_jumpbox_allowed_ips" {
  description = "List of IPs that should be allowed to jumpbox, this value is not stored in Azure Keyvault and should always be loaded from tfvars"
  default = []
}
