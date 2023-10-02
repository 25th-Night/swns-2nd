output "db_public_ip" {
  value = ncloud_public_ip.db_public_ip.public_ip
}

output "db_private_ip" {
  value = module.db.private_ip
}

output "be_private_ip" {
  value = module.be.private_ip
}

output "be_public_ip" {
  value = ncloud_public_ip.be_public_ip.public_ip
}

output "lb_domain" {
  value = module.loadBalancer.lb_domain
}
