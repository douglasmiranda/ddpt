"""
WSGI config for {{ cookiecutter.project_name }} project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""
import os
import sys

from django.core.wsgi import get_wsgi_application

# This allows easy placement of apps within the interior
# {{ cookiecutter.django_project_name }} directory.
# app_path = os.path.dirname(os.path.abspath(__file__)).replace("/config", "")
# sys.path.append(os.path.join(app_path, "{{ cookiecutter.django_project_name }}"))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "{{ cookiecutter.django_project_name }}.config.production"
)

application = get_wsgi_application()
