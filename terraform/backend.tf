terraform {
  backend "s3" {
    bucket         = "rylupague-tf-state-bucket"
    key            = "app/terraform.tfstate"
    region         = "ap-southeast-2"
    # Old: dynamodb_table = "terraform-locks" 
    # New:
    use_lockfile   = true 
    encrypt        = true
  }
}
