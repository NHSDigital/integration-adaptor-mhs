# resource "aws_route_table" "mhs_public_rt" {
#   vpc_id = aws_vpc.mhs_vpc.id
#   tags = {
#     Name = "${var.environment_id}-mhs-public-rt"
#     EnvironmentId = var.environment_id
#   }
# }

# resource "aws_route_table_association" "public_route_public_subnet" {
#   subnet_id = aws_subnet.mhs_public_subnet.id
#   route_table_id = aws_route_table.mhs_public_rt.id 
# }

# resource "aws_route" "route_public_to_igw" {
#   route_table_id = aws_route_table.mhs_public_rt.id 
#   destination_cidr_block = "0.0.0.0/0"
#   gateway_id = aws_internet_gateway.mhs_igw.id
# }
