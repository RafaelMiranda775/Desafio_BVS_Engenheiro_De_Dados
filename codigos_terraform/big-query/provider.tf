provider "google" {
  version = "3.32.0"

  credentials = file("service_account.json")

  project = var.project_id
  region  = var.region
  zone    = var.zone
}