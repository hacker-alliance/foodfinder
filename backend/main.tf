variable "gcp-project" {}
variable "region" {}
variable "zone" {}

provider "google" {
  credentials = "gcp-credentials.json"
  project     = var.gcp-project
  region      = var.region
  zone        = var.zone
}

resource "google_storage_bucket" "foodfinder" {
  name = "foodfinder"
}
data "archive_file" "api-zip" {
  type        = "zip"
  source_dir  = "${path.module}/api"
  output_path = "${path.module}/zips/api.zip"
}

resource "google_storage_bucket_object" "api-zip" {
  name   = "api.zip"
  bucket = google_storage_bucket.foodfinder.name
  source = "${path.module}/zips/api.zip"
}

resource "google_cloudfunctions_function" "api" {
  name        = "api"
  description = "api-function"
  runtime     = "nodejs10"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.foodfinder.name
  source_archive_object = google_storage_bucket_object.api-zip.name
  trigger_http          = true
  entry_point           = "handler"
}

resource "google_endpoints_service" "openapi_service" {
  service_name   = "api.endpoints.${var.gcp-project}.cloud.goog"
  project        = var.gcp-project
  openapi_config = templatefile("openapi_spec.yml", { project-id = var.gcp-project, region = var.region })
}

resource "google_cloud_run_service" "endpoints-runtime" {
  name     = "endpoints-runtime"
  location = "us-east4"

  template {
    spec {
      containers {
        image = "gcr.io/endpoints-release/endpoints-runtime-serverless:2"
      }
    }
  }
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "gcr-noauth" {
  location    = google_cloud_run_service.endpoints-runtime.location
  project     = google_cloud_run_service.endpoints-runtime.project
  service     = google_cloud_run_service.endpoints-runtime.name
  policy_data = data.google_iam_policy.noauth.policy_data
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "api-invoke" {
  project        = google_cloudfunctions_function.api.project
  region         = google_cloudfunctions_function.api.region
  cloud_function = google_cloudfunctions_function.api.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}
