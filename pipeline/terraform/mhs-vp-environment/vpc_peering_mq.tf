##############
# MQ VPC
##############

# Get details of the MQ VPC the V&P VPC will have a peering connection with
data "aws_vpc" "mq_vpc" {
  id = var.mq_vpc_id
}

# VPC peering connection
resource "aws_vpc_peering_connection" "mq_peering" {
  vpc_id = aws_vpc.mhs_vpc.id
  peer_vpc_id = data.aws_vpc.mq_vpc.id
  auto_accept = true

  accepter {
    allow_remote_vpc_dns_resolution = true
  }

  requester {
    allow_remote_vpc_dns_resolution = true
  }

  tags = {
    Name = "${var.environment_id}-mq-vpc-peering"
    EnvironmentId = var.environment_id
  }
}

# # Add a route to the MHS VPC in the MQ VPC route table
# resource "aws_route" "mq_to_mhs_route" {
#   route_table_id = data.aws_vpc.mq_vpc.main_route_table_id
#   destination_cidr_block = aws_vpc.mhs_vpc.cidr_block
#   vpc_peering_connection_id = aws_vpc_peering_connection.mq_peering.id
#   depends_on = [aws_vpc_peering_connection.mq_peering]
# }

# # Add a route to the MQ VPC in the MHS VPC route table
# resource "aws_route" "mhs_to_mq_route" {
#   route_table_id = aws_vpc.mhs_vpc.main_route_table_id
#   destination_cidr_block = data.aws_vpc.mq_vpc.cidr_block
#   vpc_peering_connection_id = aws_vpc_peering_connection.mq_peering.id
#   depends_on = [aws_vpc_peering_connection.mq_peering]
# }

resource "aws_security_group_rule" "mhs_inbound_to_mq" {
  security_group_id = aws_security_group.mhs_inbound_security_group.id
  type = "egress"
  from_port = 5671
  to_port = 5671
  protocol = "tcp"
  source_security_group_id = var.mq_sg_id
  description = "Allow requests to Amazon MQ inbound queue"
}

resource "aws_security_group_rule" "mq_from_mhs_inbound" {
  source_security_group_id = aws_security_group.mhs_inbound_security_group.id
  type = "ingress"
  from_port = 5671
  to_port = 5671
  protocol = "tcp"
  security_group_id = var.mq_sg_id
  description = "Allow AMQP from ${var.environment_id} env"
}