###################
# MHS outbound security group
###################

# MHS outbound security group
resource "aws_security_group" "mhs_outbound_security_group" {
  name = "MHS Outbound Security Group"
  description = "The security group used to control traffic for the MHS Outbound component."
  vpc_id = aws_vpc.mhs_vpc.id

  tags = {
    Name = "${var.environment_id}-mhs-outbound-sg"
    EnvironmentId = var.environment_id
  }
}

# Ingress rule to allow requests from the MHS outbound load balancer security group
resource "aws_security_group_rule" "mhs_outbound_security_group_ingress_rule" {
  security_group_id = aws_security_group.mhs_outbound_security_group.id
  type = "ingress"
  from_port = 80
  to_port = 80
  protocol = "tcp"
  source_security_group_id = aws_security_group.alb_outbound_security_group.id
  description = "Allow HTTP inbound requests from MHS outbound load balancer"
}

# Egress rule to allow requests to S3 (as ECR stores images there and we need to be
# able to get the MHS outbound image to run) and DynamoDB (as MHS outbound uses DynamoDB).
resource "aws_security_group_rule" "mhs_outbound_security_group_vpc_endpoints_egress_rule" {
  security_group_id = aws_security_group.mhs_outbound_security_group.id
  type = "egress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  prefix_list_ids = [
    aws_vpc_endpoint.s3_endpoint.prefix_list_id,
    aws_vpc_endpoint.dynamodb_endpoint.prefix_list_id]
  description = "S3 (for pulling ECR images) and DynamoDb access."
}

# Egress rule to allow requests to the MHS route service load balancer
resource "aws_security_group_rule" "mhs_outbound_security_group_route_egress_rule" {
  security_group_id = aws_security_group.mhs_outbound_security_group.id
  type = "egress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  source_security_group_id = aws_security_group.alb_route_security_group.id
  description = "Allow HTTPS outbound connections to MHS Route service LB."
}

# Egress rule to allow requests to the MHS fake spine service load balancer
resource "aws_security_group_rule" "mhs_outbound_security_group_fake_spine_egress_rule" {
  security_group_id = aws_security_group.mhs_outbound_security_group.id
  type = "egress"
  from_port = 80
  to_port = 80
  protocol = "tcp"
  source_security_group_id = aws_security_group.alb_fake_spine_security_group.id
  description = "Allow HTTPS outbound connections to MHS Fake spine service LB."
}

# Egress rule to allow requests to ECR (to pull the MHS outbound image to run)
resource "aws_security_group_rule" "mhs_outbound_security_group_ecr_egress_rule" {
  security_group_id = aws_security_group.mhs_outbound_security_group.id
  type = "egress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  source_security_group_id = aws_security_group.ecr_security_group.id
  description = "HTTPS connections to ECR endpoint."
}

# Egress rule to allow writing logs to Cloudwatch
resource "aws_security_group_rule" "mhs_outbound_security_group_cloudwatch_egress_rule" {
  security_group_id = aws_security_group.mhs_outbound_security_group.id
  type = "egress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  source_security_group_id = aws_security_group.cloudwatch_security_group.id
  description = "HTTPS connections to Cloudwatch endpoint"
}