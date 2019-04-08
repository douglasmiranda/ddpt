.PHONY: run stop enter shell format logs clean remove info help
.DEFAULT_GOAL := help

PROJECT_DIR_NAME:={{cookiecutter.django_project_name}}
ENTER_DJANGO:=docker-compose exec django
ENTER_DJANGO_ROOT:=docker-compose exec --user=root django
DJANGO_USER_UID:=$(shell id -u)

# You may want to install awk if you don't have already
# google it: Install awk in Windows|Linux|MacOS
help: ## show make targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-20s", $$1} \
		/#__danger/ {printf "\033[31m%s ", "DANGER"} \
		{gsub(/#__danger /, ""); printf "\033[0m%s\n", $$2}'

build: ## build necessary stuff for our project to run (docker images)
	@$(MAKE) clean-py || printf "\n\033[33mWasn't able to execute clean-py, maybe some file permissions issue! But build anyway.\033[0m\n\n"
	DJANGO_USER_UID=$(DJANGO_USER_UID) docker-compose build

run: ## start containers with docker-compose and attach to logs
	DJANGO_USER_UID=$(DJANGO_USER_UID) docker-compose up

rund: ## start containers with docker-compose (detached mode)
	DJANGO_USER_UID=$(DJANGO_USER_UID) docker-compose up -d

stop: ## stop all running containers for this project
	docker-compose stop

enter: ## enter the Django container (want to play freely with manage.py commands? just `make enter` and have fun)
	$(ENTER_DJANGO) sh

enter-root: ## enter the Django container as ROOT
	$(ENTER_DJANGO_ROOT) sh

shell: ## enter the Django container and run the shell_plus or shell
	$(ENTER_DJANGO) python manage.py shell_plus || $(ENTER_DJANGO) python manage.py shell

test: ## enter the running Django container and run tests with pytest
	$(ENTER_DJANGO) pytest -v --ds {{cookiecutter.django_project_name}}.config.test

debug: ## after you set the breakpoint() in your code, attach to the Django container
	docker attach $(PROJECT_DIR_NAME)_django_1

compilemessages: ## Localization: enter the running Django container and compile .po files (create .mo files)
	# For generating the .po files fist you need to enter the django container, inside your app directory and:
	# cd {{cookiecutter.django_project_name}}/core/ (for example)
	# django-admin makemessages --locale=pt_BR
	$(ENTER_DJANGO) django-admin compilemessages --locale=pt_BR

format: ## format code using Black
	@$(ENTER_DJANGO) black --exclude "migrations/*" ./$(PROJECT_DIR_NAME)

format-diff: ## see how your code will look like after being formatted with Black
	@$(ENTER_DJANGO) black --diff --exclude "migrations/*" ./$(PROJECT_DIR_NAME)

logs: ## attach to logs of containers for this project
	docker-compose logs -f

list-packages: ## list installed Python packages with pipdeptree or pip freeze. If pipdeptree is available it list possible dependencies conflicts
	$(ENTER_DJANGO) pipdeptree || $(ENTER_DJANGO) pip freeze

list-outdated: ## list outdated Python packages
	$(ENTER_DJANGO) pip list --format=columns --user --outdated

py-info: ## useful info about your Python Environment (Container)
	@printf "\n\033[33mEnvironment Variables\033[0m\n\n"
	@$(ENTER_DJANGO) printenv
	@printf "\n\033[33mPython Version\033[0m\n\n"
	@$(ENTER_DJANGO) python -V
	@printf "\n\033[33mPython Packages Installed via pipdeptree or pip freeze\033[0m\n\n"
	@$(MAKE) list-packages

clean-py: ## clean python artifacts (cache, tests, build stuff...)
	find ./$(PROJECT_DIR_NAME) -name '*.pyc' -exec rm -f {} + \
	&& find ./$(PROJECT_DIR_NAME) -name '*.pyo' -exec rm -f {} + \
	&& find ./$(PROJECT_DIR_NAME) -name '*~' -exec rm -f {} + \
	&& find ./$(PROJECT_DIR_NAME) -name '__pycache__' -exec rm -fr {} + \
	&& find ./$(PROJECT_DIR_NAME) -name '*.egg-info' -exec rm -fr {} + \
	&& find ./$(PROJECT_DIR_NAME) -name '*.egg' -exec rm -f {} +

flush-cache: ## Clear cache, in our case Redis. Using "default" connection. See `CACHES` in settings.py
	$(ENTER_DJANGO) python manage.py shell -c "from django_redis import get_redis_connection; get_redis_connection(\"default\").flushall()"

remove: ## stop running containers and remove them
	@$(MAKE) stop
	docker-compose rm -f

remove-full: ## #__danger stop and remove running containers, VOLUMES and NETWORKS associated to them
	@echo "\033[33mATTENTION!\033[0m"
	@echo "This command will remove your containers and volumes related to them."
	@read -p "Do you want to proceed? y or n: " answer; if [ "$$answer" != "y" ]; then echo "Operation Cancelled"; exit 1; fi
	docker-compose down --volumes

first-run: ## #__danger This will run migrations and create a INSECURE superuser that you should only use in dev environment
	@echo "\033[33mATTENTION!\033[0m"
	@echo "This command will execute:"
	@echo "- Django Migrations (manage.py migrate all tables will be created)"
	@echo "- Create an \033[31mINSECURE\033[0m superuser that you should only use in dev environment"
	@echo "  - Username: a"
	@echo "  - Password: a\n"

	@read -p "Do you want to proceed? y or n: " answer; if [ "$$answer" != "y" ]; then echo "Operation Cancelled"; exit 1; fi

	$(ENTER_DJANGO) python manage.py migrate
	$(ENTER_DJANGO) python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('a', 'a@a.co', 'a')"
