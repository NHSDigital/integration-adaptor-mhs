###################
# MHS route security group
###################

# MHS route service security group
resource "aws_security_group" "mhs_route_security_group" {
  name = "MHS Route Security Group"
  description = "The security group used to control traffic for the MHS Routing component."
  vpc_id = aws_vpc.mhs_vpc.id

  tags = {
    Name = "${var.environment_id}-mhs-route-sg"
    EnvironmentId = var.environment_id
  }
}

# Ingress rule to allow requests from the MHS route load balancer security group
resource "aws_security_group_rule" "mhs_route_security_group_ingress_rule" {
  security_group_id = aws_security_group.mhs_route_security_group.id
  type = "ingress"
  from_port = 80
  to_port = 80
  protocol = "tcp"
  source_security_group_id = aws_security_group.alb_route_security_group.id
  description = "Allow HTTP inbound requests from MHS route service load balancer"
}

# Egress rule to allow requests to ElastiCache
resource "aws_security_group_rule" "mhs_route_security_group_elasticache_egress_rule" {
  security_group_id = aws_security_group.mhs_route_security_group.id
  type = "egress"
  from_port = 6379
  to_port = 6379
  protocol = "tcp"
  source_security_group_id = aws_security_group.sds_cache_security_group.id
  description = "ElastiCache access (for caching SDS query results)."
}

# Egress rule to allow requests to S3 (as ECR stores images there and we need to be
# able to get the MHS route image to run)
resource "aws_security_group_rule" "mhs_route_security_group_egress_rule" {
  security_group_id = aws_security_group.mhs_route_security_group.id
  type = "egress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  prefix_list_ids = [
    aws_vpc_endpoint.s3_endpoint.prefix_list_id,
  ]
  description = "S3 access (for pulling ECR images)."
}

# Egress rule to allow requests to ECR (to pull the MHS route image to run)
resource "aws_security_group_rule" "mhs_route_security_group_ecr_egress_rule" {
  security_group_id = aws_security_group.mhs_route_security_group.id
  type = "egress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  source_security_group_id = aws_security_group.ecr_security_group.id
  description = "HTTPS connections to ECR endpoint."
}

# Egress rule to allow writing logs to Cloudwatch
resource "aws_security_group_rule" "mhs_route_security_group_cloudwatch_egress_rule" {
  security_group_id = aws_security_group.mhs_route_security_group.id
  type = "egress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  source_security_group_id = aws_security_group.cloudwatch_security_group.id
  description = "HTTPS connections to Cloudwatch endpoint"
}