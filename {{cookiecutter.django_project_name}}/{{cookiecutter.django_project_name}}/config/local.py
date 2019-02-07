"""
Local settings for {{cookiecutter.project_name}} project.

- Run in Debug mode{% if cookiecutter.use_mailhog == 'y' %}
- Use mailhog for emails via Docker
{% elif cookiecutter.use_mailhog == 'y' %}
- Use mailhog for emails{% else %}- Use console backend for emails{% endif %}
- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .base import *  # noqa

import socket

DEBUG = True
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG
# https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#secret-key
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = "SECRET-KEY-FOR-DEVELOPMENT-OF-COURSE-YOU->MUST<-USE-A-SECURE-ONE-IN-PRODUCTION-{{cookiecutter.django_project_name}}"

# Mail settings
EMAIL_PORT = 1025
{% if cookiecutter.use_mailhog == 'y' %}EMAIL_HOST = 'mailhog'{% else %}
EMAIL_HOST = 'localhost'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
{% endif %}
# django-debug-toolbar
INSTALLED_APPS += ['debug_toolbar', "django_extensions"]
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1', '10.0.2.2']

# Your local stuff: Below this line define 3rd party library settings
