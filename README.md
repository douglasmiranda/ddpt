# Django Project Template

This is a template for Django Projects. Ready to run with Docker, with development and production settings.

- [Django Project Template](#django-project-template)
  - [Features](#features)
  - [Optional Integrations](#optional-integrations)
  - [Usage](#usage)
  - [Submit a Pull Request](#submit-a-pull-request)
  - [Related links](#related-links)
    - [Docker](#docker)
    - [Python/Django](#pythondjango)
    - [Docker Images](#docker-images)
    - [Others](#others)
    - [Me](#me)

## Features

* Django 2.2 + Python 3.6/3.7
* Using Alpine Linux based images
* Setup close to production + nice dev tools when local
* Ready to use [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/) for keeping you sensitive data safe
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
  * Send emails via Anymail_ (using Mailgun_ by default, but switchable)
* Bonus: Check the `Makefile`, you'll see lots of shortcuts to speed up your development

## Optional Integrations

*These features can be enabled during initial project setup.*

* (Development) Integration with MailHog_ for local email testing
* (Production) Integration with Mailgun_ for local email testing
* (Production) Integration with Sentry_ for error logging
* (Production) Media storage using Amazon S3
* Django Admin theme


## Usage

Let's pretend you want to create a Django project called "redditclone". Rather than using `startproject`
and then editing the results to include your name, email, and various configuration issues that always get forgotten until the worst possible moment, get cookiecutter_ to do all the work.

First, get Cookiecutter. Trust me, it's awesome::

```bash
pip install "cookiecutter"
```

Now run it against this repo::

```bash
cookiecutter https://github.com/douglasmiranda/ddpt
```

You'll be prompted for some values. Provide them, then a Django project will be created for you.

**Warning**: After this point, change 'Douglas', 'douglascoding', etc to your own information.

Answer the prompts with your own desired options_. For example::

    TODO

Enter the project and take a look around::

```bash
cd reddit/
ls
```

Create a git repo and push it there::

```bash
git init
git add .
git commit -m "first awesome commit"
git remote add origin git@github.com:YOURGITHUBUSERNAME/redditclone.git
git push -u origin master
```

---

## Submit a Pull Request

Keep your pull requests small. Better yet, explain what you plan to do in the issues, it will save time in the end.

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
