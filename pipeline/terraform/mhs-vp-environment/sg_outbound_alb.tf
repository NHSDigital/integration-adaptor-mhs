# MHS outbound load balancer security group
resource "aws_security_group" "alb_outbound_security_group" {
  name = "Outbound ALB Security Group"
  description = "The security group used to control traffic for the outbound MHS Application Load Balancer."
  vpc_id = aws_vpc.mhs_vpc.id

  # Allow inbound traffic from the supplier VPC. We don't make any
  # assumptions here about the internal structure of the supplier VPC,
  # instead just allowing inbound requests from the whole VPC.
  # A supplier could restrict this rule further by limiting access, for
  # example to a specific Security Group
  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = [
      data.aws_vpc.supplier_vpc.cidr_block
    ]
    description = "Allow inbound HTTPS connections from supplier VPC"
  }

  # Allow outbound traffic to MHS outbound tasks
  egress {
    from_port = 80
    to_port = 80

    security_groups = [
      aws_security_group.mhs_outbound_security_group.id
    ]
    protocol = "tcp"
    description = "Allow downstream HTTP connections to MHS outbound tasks"
  }

  # Allow inbound traffic from the DLT VPC. We don't make any
  # assumptions here about the internal structure of the DLT VPC,
  # instead just allowing inbound requests from the whole VPC.
  # A DLT could restrict this rule further by limiting access, for
  # example to a specific Security Group
  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = [
      data.aws_vpc.dlt_vpc.cidr_block
    ]
    description = "Allow inbound HTTPS connections from DLT VPC"
  }

  tags = {
    Name = "${var.environment_id}-alb-outbound-sg"
    EnvironmentId = var.environment_id
  }
}