from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "{{cookiecutter.django_project_name}}.core"
    verbose_name = "Core"

    def ready(self):
        """Override this to put in:
            Core system checks
            Core signal registration
        """
        pass
