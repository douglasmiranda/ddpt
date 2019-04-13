# Django Project Template

This is a template for Django Projects. Ready to run with Docker, with development and production settings.

- [Django Project Template](#django-project-template)
  - [Features](#features)
  - [Optional Integrations](#optional-integrations)
  - [Usage](#usage)
    - [Introducing Cookiecutter](#introducing-cookiecutter)
    - [Start the project](#start-the-project)
    - [Running your newly created Django project](#running-your-newly-created-django-project)
      - [Note about building the Django image](#note-about-building-the-django-image)
      - [Build, run and manage with Makefile](#build-run-and-manage-with-makefile)
        - [1 - Build](#1---build)
        - [2 - Run](#2---run)
        - [3 - Firt things on first run](#3---firt-things-on-first-run)
  - [Why Am I doing things this way?](#why-am-i-doing-things-this-way)
    - [Why create a "django" user in the Django image?](#why-create-a-%22django%22-user-in-the-django-image)
      - [Unprivileged user](#unprivileged-user)
      - [Fix permissions in a shared code volume using a common UID](#fix-permissions-in-a-shared-code-volume-using-a-common-uid)
    - [Why Alpine and not Debian or Ubuntu?](#why-alpine-and-not-debian-or-ubuntu)
    - [Where's NGINX?](#wheres-nginx)
    - [Why Docker Swarm and not Docker Compose in production?](#why-docker-swarm-and-not-docker-compose-in-production)
      - [It will be familiar](#it-will-be-familiar)
      - [Advanced Deployment](#advanced-deployment)
        - [Control](#control)
        - [Automatic rollback](#automatic-rollback)
        - [Zero downtime deployment](#zero-downtime-deployment)
        - [Security](#security)
    - [Some Docker Swarm notes](#some-docker-swarm-notes)
      - [Single Node](#single-node)
      - [Multiple Nodes](#multiple-nodes)
        - [Databases and Storages](#databases-and-storages)
  - [Submit a Pull Request](#submit-a-pull-request)
  - [TODO](#todo)
  - [Related links](#related-links)
    - [Docker](#docker)
    - [Python/Django](#pythondjango)
    - [Docker Images](#docker-images)
    - [Others](#others)
    - [Me](#me)

## Features

* Django 2.2 + Python 3.6 / 3.7
* Using Alpine Linux based images
* Setup close to production + nice dev tools when local
* Ready to use [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/) for keeping your sensitive data safe
* Ready to use [Docker Configs](https://docs.docker.com/engine/swarm/configs/) if you want
* Development:
  * Build and run with Docker Compose
  * Django Extensions
  * Django Debug Toolbar
  * ipdb
  * Format code style with Black!
* Production:
  * Deploy with Docker Swarm (docker stack command)
  * Run your Django using gunicorn
  * Reverse proxy with Caddy (easy HTTPS)
  * Serve static files with Whitenoise
  * Redis for Cache and Session Storage
  * Send emails via Anymail (using Mailgun_ by default, but switchable)
* Bonus: Check the [Makefile](%7B%7Bcookiecutter.django_project_name%7D%7D/Makefile), you'll see lots of shortcuts to speed up your development

> [TODO](#todo)

## Optional Integrations

*These features can be enabled during initial project setup.*

* (Development) Integration with MailHog_ for local email testing
* (Production) Integration with Mailgun_ for local email testing
* (Production) Integration with Sentry_ for error logging
* (Production) Media storage using Amazon S3
* Django Admin theme


## Usage

### Introducing Cookiecutter

Let's pretend you want to create a Django project called "awesome_project". Rather than using `startproject`
and then editing the results to include your name, email, and various configuration issues that always get forgotten until the worst possible moment, get cookiecutter_ to do all the work.

First, get [Cookiecutter](https://github.com/audreyr/cookiecutter). Trust me, it's awesome:

```bash
pip install cookiecutter
```

### Start the project

Now run it against this repo:

```bash
cookiecutter https://github.com/douglasmiranda/ddpt
```

You'll be prompted for some values. Provide them, then a Django project will be created for you.

Answer the prompts with your own desired options. For example:

```
$ cookiecutter https://github.com/douglasmiranda/ddpt
project_name [Project Name]: Awesome Project
django_project_name [awesome_project]: awesome_project
author_name [Your Name or Company Name]: Awesome Company
email [you@example.com]: me@awesomecompany.dev
description [A short description of the project.]: An Awesome Project!
domain_name [example.com]: awesomeproject.dev
version [0.1.0]: 0.1.0
timezone [UTC]: UTC
language_code [en-us]: en-us
use_admin_theme [y]: y
use_mailgun [n]: y
use_mailhog [y]: y
use_s3 [n]: y
use_sentry_for_error_reporting [n]: y
```

Enter the project and take a look around:

```bash
~/dev
❯ cd awesome_project/

~/dev/awesome_project
❯ ls
awesome_project/  deployment/  docker-compose.yml  Dockerfile*  Makefile  manage.py*  README.md*  requirements/
```

Let's see the project structure:

```
❯ tree
.
├── awesome_project
│   ├── config
│   │   ├── base.py
│   │   ├── __init__.py
│   │   ├── local.py
│   │   ├── production.py
│   │   ├── test.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── core
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   └── core
│   │   │       └── home.html
│   │   ├── urls.py
│   │   └── views.py
│   ├── __init__.py
│   └── users
│       ├── admin.py
│       ├── apps.py
│       ├── __init__.py
│       ├── migrations
│       │   ├── 0001_initial.py
│       │   └── __init__.py
│       ├── models.py
│       ├── urls.py
│       └── views.py
├── deployment
│   ├── caddy
│   │   ├── Caddyfile
│   │   └── Dockerfile
│   ├── db-migration.yml
│   ├── django
│   │   ├── django-entrypoint.sh
│   │   └── django-health check.sh
│   ├── docker-stack.caddy.yml
│   ├── docker-stack.django.yml
│   ├── docker-stack.postgres.yml
│   ├── docker-stack.redis.yml
│   ├── Makefile
│   └── README.md
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── manage.py
├── README.md
└── requirements
    ├── base.txt
    ├── dev.txt
    └── test.txt
```

### Running your newly created Django project

If you know the basics of Docker, Docker Compose and the Django management commands (`python manage.py` / `django-admin`), you all set. But I do have one thing or two to show you in the next topics.

> [How to run](#build-run-and-manage-with-makefile)

#### Note about building the Django image

I'm using a user called `django` for this container, for production and development. This user inside the container has to match the `UID` of the host user so you don't have those permissions issues when sharing a volume between the container and your host OS. More on this subject [here](#why-docker-swarm-and-not-docker-compose-in-production).

When I'm using MAC this doesn't matter (because of how Docker for MAC works) and when I'm in Linux, my `UID` is probably the default **1000** (find with `id -u $USER`), so I think it's a good idea to set this as default. But since it's an `ARG` you can customize the build, with build args in Docker. With Docker Compose, for example:

```bash
# Let's find what's our UID
$ id -u $USER
1001
# If it's 1001:
docker-compose build --build-arg DJANGO_USER_UID=1001
```

#### Build, run and manage with Makefile

There are many commands we run all day long during development, so I made a **Makefile** that contains some good common tasks to help you get more productive. Next, we'll see what's in that Makefile.

> [Makefile](%7B%7Bcookiecutter.django_project_name%7D%7D/Makefile)

Don't fear the Makefile, it's not that weird to read. It contains common commands that we run during development, so you can change and improve to fit your daily flow.

If you run `make help` you'll see what's available for you to use.

| command                 | description                                                                                                                      |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| `help`                  | show make targets                                                                                                                |
| `build`                 | build necessary stuff for our project to run (docker images)                                                                     |
| `run`                   | start containers with docker-compose and attach to logs                                                                          |
| `rund`                  | start containers with docker-compose (detached mode)                                                                             |
| `stop`                  | stop all running containers for this project                                                                                     |
| `enter`                 | enter the Django container (want to play freely with manage.py commands? just `make enter` and have fun)                         |
| `enter-root`            | enter the Django container as ROOT                                                                                               |
| `shell`                 | enter the Django container and run the shell_plus or shell                                                                       |
| `test`                  | enter the running Django container and run tests with pytest                                                                     |
| `debug`                 | after you set the breakpoint() in your code, attach to the Django container                                                      |
| `compilemessages`       | Localization: enter the running Django container and compile .po files (create .mo files)                                        |
| `format`                | format code using Black                                                                                                          |
| `format-diff`           | see how your code will look like after being formatted with Black                                                                |
| `logs`                  | attach to logs of containers for this project                                                                                    |
| `list-packages`         | list installed Python packages with pipdeptree or pip freeze. If pipdeptree is available it list possible dependencies conflicts |
| `list-outdated`         | list outdated Python packages                                                                                                    |
| `py-info`               | useful info about your Python Environment (Container)                                                                            |
| `clean-py`              | clean python artifacts (cache, tests, build stuff...)                                                                            |
| `flush-cache`           | Clear cache, in our case Redis. Using "default" connection. See `CACHES` in settings.py                                          |
| `remove`                | stop running containers and remove them                                                                                          |
| `remove-full`           | DANGER stop and remove running containers, VOLUMES and NETWORKS associated to them                                               |
| `first-run`             | DANGER This will run migrations and create a INSECURE superuser that you should only use in dev environment                      |
| `fix-volume-permission` | Fix common volume permissions                                                                                                    |

##### 1 - Build

```
make build
```

Our build target it's basically `docker-compose build`. But it will discover our (host) user `UID` and set as the UID of the **django** user inside the container.

> [Why create a "django" user in the Django image?](#why-create-a-django-user-in-the-django-image)

##### 2 - Run

```bash
# For run attached
make run
# Run detached
make rund
```

Basically `docker-compose up`. But with the `--no-build` flag to make sure you run `make build` which takes care of the user `UID` stuff.

##### 3 - Firt things on first run

Now you can just enter the Django container:

```bash
# Using our shortcut
make enter
# Or with docker-compose
docker-compose exec django sh
```

And with `python manage.py` commands you do what you usually do. (Run migrations, create super user...)

But I do have a shortcut for this too. xD

```bash
# Using our shortcut
make first-run
```

Basically it runs migrations and add a superuser with username **a** and password **a**.

If for some reason you still have a problem with volume permissions, there's a fix in the Makefile too, just run `make fix-volume-permission`.

## Why Am I doing things this way?

Well, this is an opinionated project template, if you have more questions, don't be shy, open an issue.

Next, I'll try to answer some questions.

### Why create a "django" user in the Django image?

#### Unprivileged user

That's because it's more secure to run processes with non-privileged users. You could choose to run in development as root, but in Django we're always running commands that generate files, and you'll be doing that from inside the container, therefore creating files as root and you can't write to them with your normal host user. You'll be always executing `sudo chown ...`. Plus I'm trying to keep things close to production here.

In Linux what matters is not the human-readable user name like "django". What really matters is the `UID`, and they can differ from one Linux distribution to another, so you have to make sure to use the same `UID` for both the container user and you host user.

You can find your user `UID` with `id -u $USER`.

#### Fix permissions in a shared code volume using a common UID

As you can see in our [docker-compose.yml](%7B%7Bcookiecutter.django_project_name%7D%7D/docker-compose.yml) file we have our Django code shared with the Django container. In projects like this, we create files from outside and from inside the container, and this can lead to some permission issues in development. (Not only in dev but for our production version we apply the correct owner to the files when copying, so no problem there.)

The approach I chose here was to use your user `UID` as the `UID` of the user **django** inside the container.

If you're in Docker for MAC, you won't face that issue because it works a litte different when sharing volumes from host to user.

### Why Alpine and not Debian or Ubuntu?

Alpine Linux is great, sometimes you'll need to build something from source, discover what the proper package name and things like that, but it's more secure and lightweight, do some search and you may like.

- https://alpinelinux.org/about/

Debian, Ubuntu and other images are great too, you can make changes and use them. Just make sure to use the official images.

### Where's NGINX?

I'm using Caddy as a reverse proxy for Django, it's simple, great, full of features, easy HTTPS. Depending on the size of your project and audience, you'll probably face some other issues with optimization before you get to optimize your Web Server.

*But I will provide NGINX configs with HTTPS soon.

### Why Docker Swarm and not Docker Compose in production?

Well, you can, and maybe you should.

But let me try to convince you to use Docker Swarm even if you're running in a single node/host.

(I'll try to give some examples of practical things you get with Docker Swarm, for more detailed, advanced stuff you should really do some research on the subject.)

#### It will be familiar

You can deploy in [Docker Swarm](https://docs.docker.com/engine/swarm/) with the [docker stack](https://docs.docker.com/engine/reference/commandline/stack/) command almost the same docker-compose.yml file you're used to. There are some things you can use in one and not the other, but you'll be fine, nothing impossible to fix.

#### Advanced Deployment

##### Control

You can control resources usage, how it will be restarted if needed, health checks, replicas and more.

##### Automatic rollback

The thing about health check is that you can do auto-rollback, which is awesome. Every time you redeploy, if your new update breaks the health check, Docker will automatically rollback to the previous configuration.

##### Zero downtime deployment

If you have control of replicas, how they are started, restarted, updated and can check the health of you containers, you can enjoy zero downtime deployments.

The flow is basically:

- You make a new deployment
- With `docker stack deploy`, the replicas will start the update process
  - you can tell Docker to start the new replicas
  - make sure they are healthy
  - stop the old replicas
- If everything went ok, docker ingress network will redirect the requests to the new replicas
- If the updated replicas are not fine, the health check reported failure, Docker start the rollback to the previous settings

Of course, it can be more complicated than that, you probably need to run some simulated scenarios in order to decide if this is enough for your project.

##### Security

Learn about [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/) and stop using plain environment variables for sensitive data.

You may want to learn about connecting to Docker remotely using TLS and improve your deployment. **Do not expose Docker without configuring TLS!**

### Some Docker Swarm notes

#### Single Node

As I said before, you can enjoy Docker Swarm in a single machine, you don't need to configure a multi-node setup.

If you are in a single node, you can use volumes and don't even need to worry about replicas placement, almost just like with Docker Compose.

#### Multiple Nodes

Well, I can't possibly cover here in some notes the challenges that distributed systems bring. But I can list some specific notes to Django in a multi-node setup and Docker Swarm.

##### Databases and Storages

I won't cover clustering databases, that's really extensive.

I won't cover distributed storages either for the same reason.

But let's say your scenario is: You have to go multi-node, but only for some workers and some containers you're running, maybe it's because they are memory/CPU intensive or something like that. Your Django application, some volume, maybe the database, can stay in the same node(s) and you would like a nice solution to fit that design.

You could get something from [placement](https://docs.docker.com/compose/compose-file/#placement) in your Docker Stack/Compose files.

"Easy" solution is: Use something like S3 for storage and any database as a service from your hosting/cloud provider and go crazy on replicate and manage your application/worker containers with Docker Swarm, that way you probably will face fewer issues.

---

## Submit a Pull Request

Keep your pull requests small. Better yet, explain what you plan to do in the issues, it will save time in the end.

## TODO

- Deployment docs #6
- Deployment: Provisioning (info, examples, docs...) #2
- More info about Docker Swarm
  - maybe more information about using even if it's single node
- More information on Storages (Static/Media files) #7
  - remove / make optional whitenoise
  - alternative to S3 (maybe Minio would be nice)
  - CDN
- CI/CD docs and/or examples #3

## Related links

### Docker

- https://docs.docker.com/compose/
- https://docs.docker.com/engine/swarm/
- https://docs.docker.com/engine/swarm/secrets/
- https://docs.docker.com/engine/swarm/configs/
- https://docs.docker.com/engine/reference/commandline/stack/


### Python/Django

- https://gunicorn.org/
- https://github.com/ambv/black
- https://pypi.org/project/ipdb/
- https://whitenoise.readthedocs.io/
- https://docs.pytest.org/en/latest/
- https://github.com/anymail/django-anymail
- https://factoryboy.readthedocs.io/en/latest/
- https://pytest-django.readthedocs.io/en/latest/
- https://github.com/jazzband/django-debug-toolbar
- https://github.com/django-extensions/django-extensions

### Docker Images

- https://hub.docker.com/_/redis
- https://hub.docker.com/_/python
- https://hub.docker.com/_/postgres
- https://hub.docker.com/r/mailhog/mailhog
- https://hub.docker.com/r/douglasmiranda/caddy

### Others

- http://www.mailgun.com/
- https://caddyserver.com/
- https://letsencrypt.org/
- https://sentry.io/welcome/
- https://github.com/mailhog/MailHog
- https://github.com/audreyr/cookiecutter

### Me

- https://github.com/douglasmiranda/lab
- https://github.com/douglasmiranda/gconfigs
- https://github.com/douglasmiranda/dockerfiles
- https://github.com/douglasmiranda/django-admin-bootstrap
