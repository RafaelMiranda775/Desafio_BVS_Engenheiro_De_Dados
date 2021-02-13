# Simple Cloud Composer Environment Example

This example illustrates how to use the `composer` module.

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| composer\_env\_name | Name of Cloud Composer Environment. | `string` | n/a | yes |
| composer\_service\_account | Service Account to be used for running Cloud Composer Environment. | `string` | n/a | yes |
| project\_id | Project ID where Cloud Composer Environment is created. | `string` | n/a | yes |
| region | Region where Cloud Composer Environment is created. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| airflow\_uri | URI of the Apache Airflow Web UI hosted within the Cloud Composer Environment. |
| composer\_env\_id | ID of Cloud Composer Environment. |
| composer\_env\_name | Name of the Cloud Composer Environment. |
| gcs\_bucket | Google Cloud Storage bucket which hosts DAGs for the Cloud Composer Environment. |
| gke\_cluster | Google Kubernetes Engine cluster used to run the Cloud Composer Environment. |

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

To provision this example, run the following from within this directory:
- `terraform init` to get the plugins
- `terraform plan` to see the infrastructure plan
- `terraform apply` to apply the infrastructure build
- `terraform destroy` to destroy the built infrastructure

Service Account
A service account with the following roles must be used to provision the resources of this module:

```
- Project Editor: roles/editor
- Network Admin: roles/compute.networkAdmin
- Instance Admin: roles/compute.instanceAdmin.v1
- Service Account User: roles/iam.serviceAccountUser
- Composer Worker: roles/composer.worker
```
The Project Factory module and the IAM module may be used in combination to provision a service account with the necessary roles applied.

## APIs
A project with the following APIs enabled must be used to host the resources of this module:
```
Cloud Composer API: composer.googleapis.com
```
The Project Factory module can be used to provision a project with the necessary APIs enabled.