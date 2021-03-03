## Azure config variables ##
variable "client_id" {}

variable "client_secret" {}

variable location {
  default = "UK West"
}

variable state_bucket_storage_account {
  description = "Name of storage account with TF state bucket"
  default = "niafstate"
}

variable state_bucket_name {
  description = "Name of bucket (container) with state file"
  default = "nia-tf-state-container"
}

## Resource group variables ##
variable resource_group_name {
  default = "mhs-rg"
}

## AKS kubernetes cluster variables ##
variable cluster_name {
  default = "mhs-adaptor"
}

variable jumpbox_user {
  default = "mhs_user"
}

variable "agent_count" {
  default = 1
}

variable "dns_prefix" {
  default = "mhs"
}

variable "admin_username" {
    default = "mhs"
}

variable "jumpbox_allowed_ips" {
  default = [
    "165.225.207.72/32", # zscaler WAW
    "91.222.71.98/32",   # k gdn
    "195.89.171.5/32",   # k bfs1
    "62.254.63.50/32",   # k bfs2
    "62.254.63.52/32" ]  # k bfs3
}

variable "N3_peering_name" {
  default = "mhs_vnet-to-ZVNET-UKW-P-N3SharedService"
}

variable "N3_next_hop" {
  default = "172.17.166.116"
}

variable "N3_prefixes" {
  default = [
    "172.17.0.0/16",
    "155.231.231.0/29", # for DNS 155.231.231.1 155.231.231.2
    "10.239.0.0/16"
  ]
}

variable "N3_dns_servers" {
  default = [ "155.231.231.1", "155.231.231.2" ]
}

variable "mhs_vnet_cidr" {
  default = "172.28.65.0/24"
}

variable "mhs_aks_internal_cidr" {
  default = "10.21.0.0/16"
}

variable "mhs_aks_internal_dns" {
  default = "10.21.0.10"
}

variable "mhs_aks_docker_bridge_cidr" {
  default = "10.22.0.1/16"
}

variable use_servicebus {
  type = bool
  default = false
}

# variable "dns_servers" {
#   default = ["10.20.0.3", "10.20.0.4"]
# }

variable "aks_subnet_cidr" {
  default = "172.28.65.128/25"
}

variable "firewall_subnet_cidr" {
  default = "172.28.65.0/26"
}

variable "jumpbox_subnet_cidr" {
  default = "172.28.65.64/27"
}

variable "redis_subnet_cidr" {
  default = "172.28.65.96/28"
}


/*
vnet - 172.28.65.0/24:
- 172.28.65.0/25:
- - firewall - 172.28.65.0/26
- - 172.28.65.64/26:
- - - jumpbox 172.28.65.64/27
- - - 172.28.65.96/27:
- - - - redis 172.28.65.96/28
- - - - free  172.28.65.112/28
- aks 172.28.65.128/25
*/