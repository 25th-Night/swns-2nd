variable "ncp_access_key" {
  type = string
}

variable "ncp_secret_key" {
  type = string
}

variable "name" {
  type = string
}

variable "env" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "subnet_id" {
  type = string
}

variable "inbound_ip_block" {
  type = string
}

variable "port_range" {
  type = string
}

variable "init_script_path" {
  type = string
}

variable "init_script_envs" {
  type = map(any)
}

variable "server_image_product_code" {
  type = string
}

variable "server_product_code" {
  type = string
}
