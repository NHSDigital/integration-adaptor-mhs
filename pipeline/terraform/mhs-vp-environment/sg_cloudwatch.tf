# Security group for the Cloudwatch VPC endpoint
resource "aws_security_group" "cloudwatch_security_group" {
  name = "Cloudwatch Endpoint Security Group"
  description = "The security group used to control traffic for the Cloudwatch VPC endpoint."
  vpc_id = aws_vpc.mhs_vpc.id

  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    # Only allow incoming requests from MHS security groups
    security_groups = [
      aws_security_group.mhs_outbound_security_group.id,
      aws_security_group.mhs_route_security_group.id,
      aws_security_group.mhs_inbound_security_group.id,
      aws_security_group.mhs_fake_spine_security_group.id
    ]
    description = "Allow inbound HTTPS requests from MHS tasks"
  }

  tags = {
    Name = "${var.environment_id}-cloudwatch-endpoint-sg"
    EnvironmentId = var.environment_id
  }
}