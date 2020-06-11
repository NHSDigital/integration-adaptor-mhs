##############
# Supplier VPC
##############

# Get details of the supplier VPC the MHS VPC will have a peering connection with
data "aws_vpc" "supplier_vpc" {
  id = var.supplier_vpc_id
}

# VPC peering connection
resource "aws_vpc_peering_connection" "supplier_peering_connection" {
  peer_vpc_id = var.supplier_vpc_id
  vpc_id = aws_vpc.mhs_vpc.id
  auto_accept = true

  accepter {
    allow_remote_vpc_dns_resolution = true
  }

  requester {
    allow_remote_vpc_dns_resolution = true
  }

  tags = {
    Name = "${var.environment_id}-mhs-supplier-peering-connection"
    EnvironmentId = var.environment_id
  }
}

# Add a route to the MHS VPC in the supplier VPC route table
resource "aws_route" "supplier_to_mhs_route" {
  route_table_id = data.aws_vpc.supplier_vpc.main_route_table_id
  destination_cidr_block = aws_vpc.mhs_vpc.cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.supplier_peering_connection.id
}

# Add a route to the supplier VPC in the MHS VPC route table
resource "aws_route" "mhs_to_supplier_route" {
  route_table_id = aws_vpc.mhs_vpc.main_route_table_id
  destination_cidr_block = data.aws_vpc.supplier_vpc.cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.supplier_peering_connection.id
}

# Allow DNS resolution of the domain names defined in route53.tf in the supplier VPC
resource "aws_route53_zone_association" "supplier_hosted_zone_mhs_vpc_association" {
  zone_id = aws_route53_zone.mhs_hosted_zone.zone_id
  vpc_id = data.aws_vpc.supplier_vpc.id
}

# # Allow outbound requests from MHS inbound security group to the Amazon MQ inbound queue
# resource "aws_security_group_rule" "mhs_inbound_security_group_amazon_mq_egress_rule" {
#   security_group_id = aws_security_group.mhs_inbound_security_group.id
#   type = "egress"
#   from_port = 5671
#   to_port = 5671
#   protocol = "tcp"
#   # Not making any assumptions here about the internal structure of the supplier VPC.
#   # This can be changed and made more specific to lock this down more.
#   cidr_blocks = [
#     data.aws_vpc.supplier_vpc.cidr_block]
#   description = "Allow outbound requests to Amazon MQ inbound queue"
# }
