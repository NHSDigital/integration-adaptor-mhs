###################
# MHS inbound security group
###################

# MHS inbound security group
resource "aws_security_group" "mhs_inbound_security_group" {
  name = "MHS Inbound Security Group"
  description = "The security group used to control traffic for the MHS Inbound component."
  vpc_id = aws_vpc.mhs_vpc.id

  tags = {
    Name = "${var.environment_id}-mhs-inbound-sg"
    EnvironmentId = var.environment_id
  }
}

# Ingress rule to allow requests from the MHS inbound load balancer
resource "aws_security_group_rule" "mhs_inbound_security_group_ingress_rule" {
  security_group_id = aws_security_group.mhs_inbound_security_group.id
  type = "ingress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  # We're allowing inbound requests from the private subnets as MHS inbound load balancer
  # can't have a security group for us to reference.
  cidr_blocks = aws_subnet.mhs_subnet.*.cidr_block
  description = "Allow HTTPS inbound requests from MHS inbound load balancer"
}

# Ingress rule to allow healthcheck requests from the MHS inbound load balancer
resource "aws_security_group_rule" "mhs_inbound_security_group_healthcheck_ingress_rule" {
  security_group_id = aws_security_group.mhs_inbound_security_group.id
  type = "ingress"
  from_port = 80
  to_port = 80
  protocol = "tcp"
  cidr_blocks = aws_subnet.mhs_subnet.*.cidr_block
  description = "Allow an HTTP connection from the inbound NLB to the inbound service. For LB healthchecks."
}

# Egress rule to allow requests to S3 (as ECR stores images there and we need to be
# able to get the MHS inbound image to run) and DynamoDB (as MHS inbound uses DynamoDB).
resource "aws_security_group_rule" "mhs_inbound_security_group_egress_rule" {
  security_group_id = aws_security_group.mhs_inbound_security_group.id
  type = "egress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  prefix_list_ids = [
    aws_vpc_endpoint.s3_endpoint.prefix_list_id,
    aws_vpc_endpoint.dynamodb_endpoint.prefix_list_id]
  description = "S3 (for pulling ECR images) and DynamoDb access."
}

# Egress rule to allow requests to ECR (to pull the MHS inbound image to run)
resource "aws_security_group_rule" "mhs_inbound_security_group_ecr_egress_rule" {
  security_group_id = aws_security_group.mhs_inbound_security_group.id
  type = "egress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  source_security_group_id = aws_security_group.ecr_security_group.id
  description = "HTTPS connections to ECR endpoint."
}

# Egress rule to allow writing logs to Cloudwatch
resource "aws_security_group_rule" "mhs_inbound_security_group_cloudwatch_egress_rule" {
  security_group_id = aws_security_group.mhs_inbound_security_group.id
  type = "egress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  source_security_group_id = aws_security_group.cloudwatch_security_group.id
  description = "HTTPS connections to Cloudwatch endpoint"
}