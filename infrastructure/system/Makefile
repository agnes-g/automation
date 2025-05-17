UNAME := $(shell uname)

ENVIRONMENTS_PATH := envs
ENV ?= dev
REGION ?= eu-west-1

TF_VARS_FLAG := --var-file=$(ENVIRONMENTS_PATH)/$(ENV)/$(REGION)/terraform.tfvars
TF_INIT := terraform init -backend-config=$(ENVIRONMENTS_PATH)/$(ENV)/$(REGION)/backend.tf
TF_PLAN := terraform plan $(TF_VARS_FLAG) 
TF_APPLY := terraform apply $(TF_VARS_FLAG)
TF_DESTROY := terraform destroy $(TF_VARS_FLAG)

.PHONY: check-environment
check-environment:
ifndef ENV
	$(error ENV not defined, please run the target like: ENV=testdummy make tf-plan)
endif

.PHONY: clean
clean:
	@rm -rf .terraform

.PHONY: format
format:
	@terraform fmt --recursive

.PHONY: validate
validate:
	@terraform validate .

.PHONY: tf-init
tf-init: check-environment clean
	@$(TF_INIT)

.PHONY: tf-plan
tf-plan: check-environment tf-init 
	@$(TF_PLAN)

.PHONY: tf-apply
tf-apply: check-environment tf-init 
	@$(TF_APPLY)

.PHONY: tf-output
tf-output: check-environment tf-init 
	@terraform output

.PHONY: tf-destroy
tf-destroy: check-environment tf-init 
	@$(TF_DESTROY)
