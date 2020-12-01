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

variable "jumpbox_allowed_ips" {
  default = [
    "165.225.207.63/32", # zscaler WAW
    "91.222.71.98/32",   # k gdn
    "195.89.171.5/32",   # k bfs1
    "62.254.63.50/32",   # k bfs2
    "62.254.63.52/32" ]  # k bfs3
}

variable "nia_vnet_cidr" {
  default = "10.20.0.0/16"
}

variable "jumpbox_subnet_cidr" {
  default = "10.20.1.0/24"
}

# Secrets 

variable "secret_mhs_partykey" {
  type = string
}