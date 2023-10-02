output "vpc_id" {
  value = ncloud_vpc.vpc.id
}

output "ipv4_cidr_block" {
  value = ncloud_vpc.vpc.ipv4_cidr_block
}
