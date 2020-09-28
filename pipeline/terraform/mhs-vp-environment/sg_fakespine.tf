###################
# MHS fake spine security group
###################

# MHS fake spine service security group
resource "aws_security_group" "mhs_fake_spine_security_group" {
  name = "MHS Fake Spine Security Group"
  description = "The security group used to control traffic for the MHS Fake Spine component."
  vpc_id = aws_vpc.mhs_vpc.id

  tags = {
    Name = "${var.environment_id}-mhs-fake-spine-sg"
    EnvironmentId = var.environment_id
  }
}

# Ingress rule to allow requests from the MHS fake spine load balancer
resource "aws_security_group_rule" "mhs_fake_spine_security_group_ingress_rule" {
  security_group_id = aws_security_group.mhs_fake_spine_security_group.id
  type = "ingress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  # We're allowing fake spine requests from the private subnets as MHS fake spine load balancer
  # can't have a security group for us to reference.
  cidr_blocks = aws_subnet.mhs_subnet.*.cidr_block
  description = "Allow HTTPS fake spine requests from MHS fake spine load balancer"
}

# Ingress rule to allow healthcheck requests from the MHS fake spine load balancer
resource "aws_security_group_rule" "mhs_fake_spine_security_group_healthcheck_ingress_rule" {
  security_group_id = aws_security_group.mhs_fake_spine_security_group.id
  type = "ingress"
  from_port = 80
  to_port = 80
  protocol = "tcp"
  cidr_blocks = aws_subnet.mhs_subnet.*.cidr_block
  description = "Allow an HTTP connection from the fake spine NLB to the fake spine service. For LB healthchecks."
}

# Egress rule to allow requests to S3 (as ECR stores images there and we need to be
# able to get the MHS fake spine image to run) and DynamoDB (as MHS fake spine uses DynamoDB).
resource "aws_security_group_rule" "mhs_fake_spine_security_group_egress_rule" {
  security_group_id = aws_security_group.mhs_fake_spine_security_group.id
  type = "egress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  prefix_list_ids = [
    aws_vpc_endpoint.s3_endpoint.prefix_list_id,
    aws_vpc_endpoint.dynamodb_endpoint.prefix_list_id]
  description = "S3 (for pulling ECR images) and DynamoDb access."
}

# Egress rule to allow requests to ECR (to pull the MHS fake spine image to run)
resource "aws_security_group_rule" "mhs_fake_spine_security_group_ecr_egress_rule" {
  security_group_id = aws_security_group.mhs_fake_spine_security_group.id
  type = "egress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  source_security_group_id = aws_security_group.ecr_security_group.id
  description = "HTTPS connections to ECR endpoint."
}

# fake-spine -> mhs inbound
# inbound lb does not have a security group, allowing traffic within the subnet
resource "aws_security_group_rule" "mhs_fake_spine_security_group_egress_inbound_app_port" {
  security_group_id = aws_security_group.mhs_fake_spine_security_group.id 
  type = "egress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  cidr_blocks = aws_subnet.mhs_subnet.*.cidr_block
  description = "Allow egress 443 outbound requests to MHS inbound"
}

# Egress rule to allow writing logs to Cloudwatch
resource "aws_security_group_rule" "mhs_fake_spine_security_group_cloudwatch_egress_rule" {
  security_group_id = aws_security_group.mhs_fake_spine_security_group.id
  type = "egress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  source_security_group_id = aws_security_group.cloudwatch_security_group.id
  description = "HTTPS connections to Cloudwatch endpoint"
}