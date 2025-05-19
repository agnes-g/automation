terraform {
  backend "s3" {
    encrypt      = true
    use_lockfile = true

    assume_role = {
      role_arn = "arn:aws:iam::654654380708:role/system-role"
    }
  }

  required_version = "1.11.4"
}
