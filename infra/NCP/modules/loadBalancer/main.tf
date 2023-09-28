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

resource "ncloud_lb_target_group" "tg" {
  name        = "${var.name}-tg-${var.env}"
  vpc_no      = var.vpc_id
  protocol    = "PROXY_TCP"
  target_type = "VSVR"
  port        = 8000
  health_check {
    protocol       = "TCP"
    port           = 8000
    cycle          = 30
    up_threshold   = 2
    down_threshold = 2
  }
  algorithm_type = "RR"
}

resource "ncloud_lb_target_group_attachment" "tg-att" {
  target_group_no = ncloud_lb_target_group.tg.target_group_no
  target_no_list = [
    var.server_instance_no
  ]
}

resource "ncloud_lb" "load_balancer" {
  name         = "${var.name}-lb-${var.env}"
  network_type = "PUBLIC"
  type         = "NETWORK_PROXY"
  subnet_no_list = [
    var.subnet_id
  ]
}

resource "ncloud_lb_listener" "lb_listner" {
  load_balancer_no = ncloud_lb.load_balancer.load_balancer_no
  protocol         = "TCP"
  port             = 80
  target_group_no  = ncloud_lb_target_group.tg.target_group_no
}
