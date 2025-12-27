- After cloning the repo:

```bash
cd terraform-backend
```

- Do terraform init

```bash
terraform init
```

- Import the existing resources (since the s3 backend and dynamodb are already created)

```bash
terraform import aws_s3_bucket.terraform_state rylupague-tf-state-bucket
terraform import aws_dynamodb_table.terraform_locks terraform-locks
terraform import aws_s3_bucket_server_side_encryption_configuration.encryption rylupague-tf-state-bucket
terraform import aws_s3_bucket_versioning.versioning rylupague-tf-state-bucket
```

- When doing `terraform plan` You should now see:

```bash
No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.
```
