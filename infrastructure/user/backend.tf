terraform {
  backend "s3" {
    encrypt      = true
    use_lockfile = true
  }

  required_version = "1.11.4"
}
