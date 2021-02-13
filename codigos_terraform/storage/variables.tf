variable "project_id" {
  description = "Bucket project id."
  type        = string
  default    = "desafio-bvs-304714"
}

variable "region" {
  description = "Bucket region"
  type        = string
  default    = "us-east1"
}

variable "zone" {
  description = "Bucket zone"
  type        = string
  default    = "us-east1-a"
}

variable "location" {
  description = "Bucket location"
  type        = string
  default    = "us-east1"
}

variable "storage_class" {
  description = "Bucket storage class"
  type        = string
  default    = "Standard"
}

variable "prefix" {
  description = "Bucket prefix"
  type        = string
  default    = ""
}

variable "name" {
  description = "Bucket name"
  type        = list
  default    = ["desafio-bvs"]
}

variable "folders" {
  description = "Bucket folders"
  type        = map
  default    = {
    desafio-bvs = ["bill_of_materials",
               "cloud_function",
               "comp_boss",
               "dags",
               "price_quote",
               "pyspark"
                              ]
  }
}

