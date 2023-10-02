terraform {
  required_providers {
    ncloud = {
      source = "NaverCloudPlatform/ncloud"
    }
  }

  required_version = ">= 0.13"

  backend "s3" {
    shared_credentials_file     = "~/.ncloud/credentials"
    bucket                      = "tf-backend"
    key                         = "swns/ncloud/staging/terraform.tfstate"
    region                      = "kr-standard"
    endpoint                    = "https://kr.object.ncloudstorage.com"
    skip_region_validation      = true
    skip_credentials_validation = true
  }
}

provider "ncloud" {
  access_key  = var.ncp_access_key
  secret_key  = var.ncp_secret_key
  region      = "KR"
  site        = "public"
  support_vpc = true
}

locals {
  env                 = "k8s"
  name                = "swns"
  vpc_ipv4_cidr_block = "10.0.0.0/16"
  subnet_netnum       = 1
  subnet_type         = "PUBLIC" # PRIVATE 설정 시, PUBLIC_IP 사용 및 SSH 자동 설치 불가
  usage_type          = "GEN"
  lb_name             = "lb"
  lb_subnet_netnum    = 2
  lb_subnet_type      = "PRIVATE"
  lb_usage_type       = "LOADB"
}

data "ncloud_nks_versions" "version" {
  filter {
    name   = "value"
    values = ["1.25.8"] # k8s는 버전 업데이트가 빨라서 최신 버전으로 지정해야 함
    regex  = true
  }
}

data "ncloud_server_image" "image" {
  filter {
    name   = "product_name"
    values = ["ubuntu-20.04"]
  }
}

data "ncloud_server_product" "product" {
  server_image_product_code = data.ncloud_server_image.image.product_code

  filter {
    name   = "product_type"
    values = ["STAND"]
  }

  filter {
    name   = "cpu_count"
    values = [2]
  }

  filter {
    name   = "memory_size"
    values = ["8GB"]
  }

  filter {
    name   = "product_code"
    values = ["SSD"]
    regex  = true
  }
}

module "vpc" {
  source = "../../modules/vpc"

  ncp_access_key  = var.ncp_access_key
  ncp_secret_key  = var.ncp_secret_key
  name            = local.name
  env             = local.env
  ipv4_cidr_block = local.vpc_ipv4_cidr_block
}

module "subnet" {
  source = "../../modules/subnet"

  ncp_access_key = var.ncp_access_key
  ncp_secret_key = var.ncp_secret_key
  name           = local.name
  env            = local.env
  vpc_id         = module.vpc.vpc_id
  subnet_netnum  = local.subnet_netnum
  subnet_type    = local.subnet_type
  usage_type     = local.usage_type
}

module "lb-subnet" {
  source = "../../modules/subnet"

  ncp_access_key = var.ncp_access_key
  ncp_secret_key = var.ncp_secret_key
  name           = local.lb_name
  env            = local.env
  vpc_id         = module.vpc.vpc_id
  subnet_netnum  = local.lb_subnet_netnum
  subnet_type    = local.lb_subnet_type
  usage_type     = local.lb_usage_type
}


module "cluster" {
  source = "../../modules/cluster"

  ncp_access_key = var.ncp_access_key
  ncp_secret_key = var.ncp_secret_key
  name           = local.name
  env            = local.env
  vpc_id         = module.vpc.vpc_id
  lb_subnet_id   = module.lb-subnet.subnet_id
  subnet_id      = module.subnet.subnet_id
  k8s_version    = data.ncloud_nks_versions.version.versions.0.value
}

module "node_pool" {
  source = "../../modules/node_pool"

  ncp_access_key             = var.ncp_access_key
  ncp_secret_key             = var.ncp_secret_key
  name                       = local.name
  env                        = local.env
  cluster_uuid               = module.cluster.cluster_uuid
  ncloud_server_product_code = data.ncloud_server_product.product.product_code
}
