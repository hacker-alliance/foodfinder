variable "tenancy_ocid" {}
variable "user_ocid" {}
variable "fingerprint" {}
variable "private_key_path" {}
variable "region" {}
variable "autonomous_database_admin_password" {}


provider "oci" {
  region           = "${var.region}"
  tenancy_ocid     = "${var.tenancy_ocid}"
  user_ocid        = "${var.user_ocid}"
  fingerprint      = "${var.fingerprint}"
  private_key_path = "${var.private_key_path}"

}
resource "oci_identity_compartment" "foodfinder" {
  #Required
  compartment_id = "${var.tenancy_ocid}"
  description    = "foodfinder compartment"
  name           = "foodfinder"
}

resource "oci_database_autonomous_database" "foodfinderDB" {
  #Required
  admin_password           = "${var.autonomous_database_admin_password}"
  compartment_id           = "${oci_identity_compartment.foodfinder.id}"
  cpu_core_count           = "1"
  data_storage_size_in_tbs = "1"
  db_name                  = "foodfinderDB"
  display_name             = "foodfinderDB"
  is_free_tier             = "true"
}

resource "oci_core_vcn" "foodfinder_vcn" {
  display_name   = "foodfinder_vcn"
  dns_label      = "foodfinder"
  cidr_block     = "10.0.0.0/16"
  compartment_id = "${oci_identity_compartment.foodfinder.id}"
}

resource "oci_core_subnet" "public_subnet" {
  display_name   = "public_subnet"
  dns_label      = "public"
  cidr_block     = "10.0.0.0/24"
  vcn_id         = "${oci_core_vcn.foodfinder_vcn.id}"
  compartment_id = "${oci_identity_compartment.foodfinder.id}"
}

resource "oci_functions_application" "foodfinder_app" {
  #Required
  compartment_id = "${oci_identity_compartment.foodfinder.id}"
  display_name   = "foodfinder_app"
  subnet_ids     = ["${oci_core_subnet.public_subnet.id}"]
}

resource "oci_core_internet_gateway" "public_internet_gateway" {
  #Required
  compartment_id = "${oci_identity_compartment.foodfinder.id}"
  vcn_id         = "${oci_core_vcn.foodfinder_vcn.id}"
  display_name   = "public_internet_gateway"
}

resource "oci_core_route_table" "public_route_table" {
  compartment_id = "${oci_identity_compartment.foodfinder.id}"
  display_name   = "public_route_table"
  vcn_id         = "${oci_core_vcn.foodfinder_vcn.id}"

  route_rules {
    network_entity_id = "${oci_core_internet_gateway.public_internet_gateway.id}"
    destination       = "0.0.0.0/0"
  }
}

resource "oci_core_route_table_attachment" "public_route_table_attachment" {
  #Required 
  subnet_id      = "${oci_core_subnet.public_subnet.id}"
  route_table_id = "${oci_core_route_table.public_route_table.id}"
}
resource "oci_apigateway_gateway" "backend_apigateway" {
  compartment_id = "${oci_identity_compartment.foodfinder.id}"
  endpoint_type  = "PUBLIC"
  display_name   = "backend_apigateway"
  subnet_id      = "${oci_core_subnet.public_subnet.id}"
}
data "oci_functions_functions" "foodfinder_api_function" {
  application_id = "${oci_functions_application.foodfinder_app.id}"
  display_name   = "api"
}

resource "oci_apigateway_deployment" "public_deployment" {
  compartment_id = "${oci_identity_compartment.foodfinder.id}"
  gateway_id     = "${oci_apigateway_gateway.backend_apigateway.id}"
  path_prefix    = "/api"

  specification {
    routes {
      methods = ["GET"]
      path    = "/"
      backend {
        type        = "ORACLE_FUNCTIONS_BACKEND"
        function_id = "${data.oci_functions_functions.foodfinder_api_function.functions[0].id}"
      }
    }
  }
}

output "APIGatewayHostname" {
  value = "${oci_apigateway_gateway.backend_apigateway.hostname}"
}
