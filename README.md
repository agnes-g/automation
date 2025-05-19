# Automation

This repository contains infrastructure automation scripts and configurations.

## Prerequisites

- [mise](https://mise.jdx.dev/) - Runtime version manager

## Getting Started

This project uses [mise](https://mise.jdx.dev/) to manage tool versions and provide consistent development environments. The configuration is in the `mise.toml` file.

### Installation

1. Install mise following the [official instructions](https://mise.jdx.dev/getting-started.html)
2. Clone this repository
3. Run `mise install` in the repository root to install the required tools

### Available Tools

- Terraform 1.11.4

### Environment Variables

The mise configuration sets the following environment variables:

- `TF_CLI_ARGS_plan="-compact-warnings"` - Reduces verbosity of terraform plan
- `TF_CLI_ARGS_apply="-compact-warnings"` - Reduces verbosity of terraform apply

### Project-Specific Configurations

- `infrastructure-system` - Configuration for the system infrastructure
- `infrastructure-user` - Configuration for the user infrastructure

### Available Tasks

You can run the following tasks using `mise run <task>`:

- `format` - Format Terraform code
- `validate` - Validate Terraform code
- `plan-system` - Run terraform plan for the system infrastructure
- `apply-system` - Run terraform apply for the system infrastructure
- `plan-user` - Run terraform plan for the user infrastructure
- `apply-user` - Run terraform apply for the user infrastructure

## Project Structure

- `infrastructure/system/` - System-level infrastructure
- `infrastructure/user/` - User-level infrastructure
