provider "google" {
  credentials = "service_account.json"
  project = var.project_id
  region = var.region
  zone    = var.zone
}