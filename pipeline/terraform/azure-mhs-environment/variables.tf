## Azure config variables ##
variable "client_id" {}

variable "client_secret" {}

variable location {
  default = "UK West"
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
  default = 3
}

variable "dns_prefix" {
  default = "mhs"
}

variable "admin_username" {
    default = "mhs"
}

variable "mhs_vnet_cidr" {
  default = "10.20.0.0/16"
}

variable "mhs_aks_internal_cidr" {
  default = "10.21.0.0/16"
}

variable "mhs_aks_internal_dns" {
  default = "10.21.0.10"
}

variable "mhs_aks_docker_bridge_cidr" {
  default = "172.17.0.1/16"
}

variable "dns_servers" {
  default = ["10.20.0.3", "10.20.0.4"]
}

variable "aks_subnet_cidr" {
  default = "10.20.2.0/23"
}

variable "firewall_subnet_cidr" {
  default = "10.20.4.0/24"
}

variable "jumpbox_subnet_cidr" {
  default = "10.20.5.0/24"
}



# variable "pods_subnet_cidr" {
#   default = "10.20.2.0/24"
# }

# variable "services_subnet_cidr" {
#   default = "10.20.3.0/24"
# }