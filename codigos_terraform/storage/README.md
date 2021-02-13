# Simple Example

This example illustrates how to use the `simple-bucket` submodule.

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| name | Name of the buckets to create. | string | n/a | yes |
| project\_id | The ID of the project in which to provision resources. | string | n/a | yes |

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

To provision this example, run the following from within this directory:
- `terraform init` to get the plugins
- `terraform plan` to see the infrastructure plan
- `terraform apply` to apply the infrastructure build
- `terraform destroy` to destroy the built infrastructure

## Service Account
User or service account credentials with the following roles must be used to provision the resources of this module:
```
Storage Admin: roles/storage.admin
```
The Project Factory module and the IAM module may be used in combination to provision a service account with the necessary roles applied.

## APIs
A project with the following APIs enabled must be used to host the resources of this module:

Google Cloud Storage JSON API: storage-api.googleapis.com
The Project Factory module can be used to provision a project with the necessary APIs enabled.
