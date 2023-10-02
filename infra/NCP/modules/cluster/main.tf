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

resource "ncloud_login_key" "loginkey" {
  key_name = "${var.name}-login-key-${var.env}"
}

resource "local_file" "private_key" {
  filename        = "./${ncloud_login_key.loginkey.key_name}.pem"
  content         = ncloud_login_key.loginkey.private_key
  file_permission = "0400"
}

resource "ncloud_nks_cluster" "cluster" {
  cluster_type         = "SVR.VNKS.STAND.C002.M008.NET.SSD.B050.G002"
  k8s_version          = var.k8s_version
  login_key_name       = ncloud_login_key.loginkey.key_name
  name                 = "${var.name}-cluster-${var.env}"
  lb_private_subnet_no = var.lb_subnet_id
  kube_network_plugin  = "cilium"
  subnet_no_list = [
    var.subnet_id
  ]
  public_network = true
  vpc_no         = var.vpc_id
  zone           = "KR-2"
  log {
    audit = true
  }
}
