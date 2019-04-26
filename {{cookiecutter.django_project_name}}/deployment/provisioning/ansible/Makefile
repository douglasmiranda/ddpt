.PHONY: help ssh-copy-id
.DEFAULT_GOAL:=help

help: ## show make targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-30s", $$1} \
		/#__danger/ {printf "\033[31m%s ", "DANGER"} \
		{gsub(/#__danger /, ""); printf "\033[0m%s\n", $$2}'

ansible-initial-setup-as-root: ## Initial setup with root password (will execute tasks with initial-setup tag; basic deploy user creation)
	ansible-playbook ansible/site.yml -i ansible/hosts.yml --ask-vault-pass -e ansible_user=root --tags=initial-setup

ansible-setup-as-deploy-user: ## Log in as deploy user and configure your host
	ansible-playbook ansible/site.yml -i ansible/hosts.yml --skip-tags=initial-setup --ask-vault-pass

instructions: ## Instructions for your provisioning steps.
	echo "Check README.md file for detailed instructions."
