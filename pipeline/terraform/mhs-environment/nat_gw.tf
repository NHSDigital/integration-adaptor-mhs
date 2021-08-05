# resource "aws_eip" "mhs_nat_gw_eip" {
#   vpc = true
#   tags = {
#     Name = "${var.environment_id}-mhs-nat_gw_eip"
#     EnvironmentId = var.environment_id
#   }
# }

# resource "aws_nat_gateway" "mhs_nat_gw" {
#   subnet_id = aws_subnet.mhs_public_subnet.id
#   allocation_id = aws_eip.mhs_nat_gw_eip.id

#   tags = {
#     Name = "${var.environment_id}-mhs-nat_gw"
#     EnvironmentId = var.environment_id
#   }
# }
