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

resource "oci_database_autonomous_database" "foodfinderDB" {
  #Required
  admin_password           = "${var.autonomous_database_admin_password}"
  compartment_id           = "${var.tenancy_ocid}"
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
  compartment_id = "${var.tenancy_ocid}"
}
