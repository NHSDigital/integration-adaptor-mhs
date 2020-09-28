# MHS route load balancer security group
resource "aws_security_group" "alb_route_security_group" {
  name = "Route ALB Security Group"
  description = "The security group used to control traffic for the MHS routing component Application Load Balancer."
  vpc_id = aws_vpc.mhs_vpc.id

  # Allow inbound traffic from MHS outbound
  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    security_groups = [
      aws_security_group.mhs_outbound_security_group.id
    ]
    description = "Allow inbound HTTPS connections from MHS outbound tasks"
  }

  # Allow outbound traffic to MHS route tasks
  egress {
    from_port = 80
    to_port = 80

    security_groups = [
      aws_security_group.mhs_route_security_group.id
    ]
    protocol = "tcp"
    description = "Allow downstream HTTP connections to MHS route tasks"
  }

  tags = {
    Name = "${var.environment_id}-alb-route-sg"
    EnvironmentId = var.environment_id
  }
}