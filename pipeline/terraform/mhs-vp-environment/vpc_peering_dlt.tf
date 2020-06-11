##############
# DLT- Distributed Load Tester VPC
##############

# Get details of the DLT VPC the V&P VPC will have a peering connection with
data "aws_vpc" "dlt_vpc" {
  id = var.dlt_vpc_id
}

# VPC peering connection
resource "aws_vpc_peering_connection" "dlt_peering_connection" {
  peer_vpc_id = var.dlt_vpc_id
  vpc_id = aws_vpc.mhs_vpc.id
  auto_accept = true

  accepter {
    allow_remote_vpc_dns_resolution = true
  }

  requester {
    allow_remote_vpc_dns_resolution = true
  }

  tags = {
    Name = "${var.environment_id}-mhs-dlt-peering-connection"
    EnvironmentId = var.environment_id
  }
}

# Add a route to the MHS VPC in the DLT VPC route table
resource "aws_route" "dlt_to_mhs_route" {
  route_table_id = data.aws_vpc.dlt_vpc.main_route_table_id
  destination_cidr_block = aws_vpc.mhs_vpc.cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.dlt_peering_connection.id
}

# Add a route to the DLT VPC in the MHS VPC route table
resource "aws_route" "mhs_to_dlt_route" {
  route_table_id = aws_vpc.mhs_vpc.main_route_table_id
  destination_cidr_block = data.aws_vpc.dlt_vpc.cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.dlt_peering_connection.id
}

# Allow DNS resolution of the domain names defined in route53.tf in the DLT VPC
resource "aws_route53_zone_association" "DLT_hosted_zone_mhs_vpc_association" {
  zone_id = aws_route53_zone.mhs_hosted_zone.zone_id
  vpc_id = data.aws_vpc.dlt_vpc.id
}
