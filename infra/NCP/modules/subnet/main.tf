terraform {
  required_providers {
    ncloud = {
      source = "NaverCloudPlatform/ncloud"
    }
  }
  required_version = ">= 0.13"
}

provider "ncloud" {
  access_key  = var.ncp_access_key
  secret_key  = var.ncp_secret_key
  region      = "KR"
  site        = "public"
  support_vpc = true
}

data "ncloud_vpc" "vpc" {
  id = var.vpc_id
}

resource "ncloud_subnet" "subnet" {
  vpc_no         = data.ncloud_vpc.vpc.id
  subnet         = cidrsubnet(data.ncloud_vpc.vpc.ipv4_cidr_block, 8, var.subnet_netnum) // subnet_netnum : 1, 2, ..
  zone           = "KR-2"
  network_acl_no = data.ncloud_vpc.vpc.default_network_acl_no
  subnet_type    = var.subnet_type // PUBLIC(Public) | PRIVATE(Private)
  name           = "${var.name}-subnet-${var.env}"
  usage_type     = var.usage_type // GEN(General) | LOADB(For load balancer)
}
