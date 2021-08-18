resource "aws_internet_gateway" "mhs_igw" {
  vpc_id = aws_vpc.mhs_vpc.id
  tags = {
    Name = "${var.environment_id}-mhs-igw"
    EnvironmentId = var.environment_id
  }
}
