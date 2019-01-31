django_project_name = "{{ cookiecutter.django_project_name }}"

if hasattr(django_project_name, "isidentifier"):
    assert (
        django_project_name.isidentifier()
    ), "Project slug should be valid Python identifier!"
