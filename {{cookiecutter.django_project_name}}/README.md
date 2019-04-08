# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Settings

Moved to {{cookiecutter.django_project_name}}/config. Check the files: base.py, local.py, production.py and test.py.

## Basic Commands

You can use the shortcuts from Makefile. Type ``make`` on your terminal in this (same dir as the README) directory, and you'll see all available targets.

### Test coverage


{% if cookiecutter.use_mailhog == "y" %}
### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server `MailHog`_ with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check cookiecutter-django Docker documentation for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``
{% endif %}

{% if cookiecutter.use_sentry_for_error_reporting == "y" %}
### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.
{% endif %}

## Deployment

Check [deployment/](deployment/README.md).
