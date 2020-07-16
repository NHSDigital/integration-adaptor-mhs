###################
# SDS cache security group
###################

# SDS cache security group
resource "aws_security_group" "sds_cache_security_group" {
  name = "SDS Cache Security Group"
  description = "The security group used to control traffic for the SDS cache endpoint."
  vpc_id = aws_vpc.mhs_vpc.id

  ingress {
    from_port = 6379
    to_port = 6379
    protocol = "tcp"
    # Only allow incoming requests from MHS route service security group
    security_groups = [
      aws_security_group.mhs_route_security_group.id
    ]
    description = "Allow Redis requests from MHS route task"
  }

  tags = {
    Name = "${var.environment_id}-sds-cache-sg"
    EnvironmentId = var.environment_id
  }
}