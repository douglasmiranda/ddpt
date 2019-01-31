.PHONY: help
.DEFAULT_GOAL := help

# You may want to install awk if you don't have already
# google it: Install awk in Windows|Linux|MacOS
help: ## show make targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-20s", $$1} \
		/#__danger/ {printf "\033[31m%s ", "DANGER"} \
		{gsub(/#__danger /, ""); printf "\033[0m%s\n", $$2}'

format: ## format code using Black (https://github.com/ambv/black)
	poetry run black ./{{cookiecutter.django_project_name}} ./hooks

format-diff: ## show how the code will be formatted with Black
	poetry run black ./{{cookiecutter.django_project_name}} ./hooks

list-outdated: ## show outdated packages from requirement files of this project
	poetry run pip list --outdated
