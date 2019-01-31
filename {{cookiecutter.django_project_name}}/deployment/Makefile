.PHONY: run stop enter shell format logs clean remove info help
.DEFAULT_GOAL := help

# Using the project name
STACK_NAME:={{cookiecutter.django_project_name}}

# You may want to install awk if you don't have already
# google it: Install awk in Windows|Linux|MacOS
help: ## show make targets
	@grep -E '^[a-zA-Z_%-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-20s", $$1} \
		/#__danger/ {printf "\033[31m%s ", "DANGER"} \
		{gsub(/#__danger /, ""); printf "\033[0m%s\n", $$2}'

define proceed_or_not
	@read -p "Do you want to proceed? y or n: " answer; if [[ "$$answer" != "y" ]]; then echo "Operation Cancelled"; exit 1; fi
endef

deployable: ## Show what's available to be deployed
	@files=`find . -type f -name "docker-stack.*.yml"`;\
	for file in $$files; do \
		printf "\033[36m%-30s" "make deploy-`echo $$file | cut -f 3 -d '.'`" ; \
		printf "\033[0m will deploy services from %s\n" $$file; \
	done

# Usage:
# You must create inside this directory a Compose file using the name pattern
# docker-stack.*.yml, for example:
# docker-stack.caddy.yml
# Then you'll be able to deploy using this Makefile simply by typing:
# make deploy-caddy
# This will match docker-stack.caddy.yml, because docker-stack.>>>caddy<<<.yml.
# Finally your services defined in docker-stack.caddy.yml will be deployed using
# the `docker stack` command
deploy-%: ## Deploy services of the chosen Compose file. Type "make deployable" and see what's available for deploying.
	@echo "\033[33mDeploying services from docker-stack.$*.yml\033[0m"
	docker stack deploy --compose-file="docker-stack.$*.yml" $(STACK_NAME)

deploy-all: ## Deploy every service available
	@files=`find . -type f -name "docker-stack.*.yml" | cut -f 3 -d '.'`;\
	for file in $$files; do \
		$(MAKE) deploy-$$file; \
	done

stack-rm: ## #__danger This will stop and remove your running containers (won't remove volumes)
	@echo "\033[31mATTENTION!\033[0m"
	@echo "This will stop and remove your running containers (won't remove volumes)"
	$(call proceed_or_not)
	docker stack rm $(STACK_NAME)

# Depending on how you deploy, you may want to build some artifacts before deploying
# - Docker images
# - Compile things
# - Do some cleaning
# But hopefully you already do these things in your CI/CD.
build: ## Build things you need before deployment
	@echo "\033[34mBuilding things for deployment\033[0m"
	# TODO
	# For example:
	# docker build --target=production -t {{cookiecutter.django_project_name}}/django .

migrate: ## ATTENTION! Execute the databases migrations, check: ./db-migration.yml
	docker stack deploy --compose-file=db-migration.yml $(STACK_NAME)
	@echo "Check if everything went ok with: \033[33mmake migration-logs\033[0m"

migration-logs: ## Follow the live logs of your latest migration. (given you already performed "make migrate")
	docker service logs -f $(STACK_NAME)_django-migrate
