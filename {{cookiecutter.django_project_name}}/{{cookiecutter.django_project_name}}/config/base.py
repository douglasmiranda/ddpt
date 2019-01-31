"""
Base settings for {{cookiecutter.project_name}} project.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
from pathlib import Path

from gconfigs import envs

DEBUG = False

# Splitting INSTALLED_APPS into separated 'categories'
DJANGO_APPS = [
    # Default Django apps:
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Useful template tags:
    # 'django.contrib.humanize',
    {% if cookiecutter.use_admin_theme == 'y' %}'bootstrap_admin', # always before django.contrib.admin{% endif %}
    # Admin
    "django.contrib.admin",
]
THIRD_PARTY_APPS = [
    # put your third party apps here
]
# Apps specific for this project go here.
LOCAL_APPS = [
    # "{{cookiecutter.django_project_name}}.core.apps.CoreConfig",
    # custom users app
    "{{cookiecutter.django_project_name}}.core.apps.CoreConfig",
    "{{cookiecutter.django_project_name}}.users.apps.UsersConfig",
    # Your stuff: custom apps go here
]
# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""{{cookiecutter.author_name}}""", "{{cookiecutter.email}}")]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # it's kinda common to use db name same as the postgres user
        "NAME": envs("POSTGRES_DB", default=None) or envs("POSTGRES_USER", default="postgres"),
        "USER": envs("POSTGRES_USER", default="postgres"),
        # allow empty pass, but will enforce non-empty password on production.py
        "PASSWORD": envs("POSTGRES_PASSWORD", default=""),
        "HOST": envs("POSTGRES_HOST", default="postgres"),
        "PORT": envs("POSTGRES_PORT", default="5432"),
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": 60,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
TIME_ZONE = envs("TIME_ZONE", default="UTC")
LANGUAGE_CODE = envs("LANGUAGE_CODE", default="en-us")
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = envs("STATIC_URL", default="/static/")
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = Path(envs("HOMEAPP")) / Path("media-root/")
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = envs("MEDIA_URL", default="/media/")

ROOT_URLCONF = "{{cookiecutter.django_project_name}}.config.urls"

# TEMPLATES
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [],
        'OPTIONS': {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "{{cookiecutter.django_project_name}}.config.wsgi.application"

# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = "users.User"
# LOGIN_REDIRECT_URL = 'core-user:redirect'
# LOGIN_URL = 'account_login'

# Location of root django.contrib.admin URL, use {% raw %}{% url 'admin:index' %}{% endraw %}
ADMIN_URL = envs("ADMIN_URL", default="admin/")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": envs("REDIS_URL", default="redis://redis:6379") + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,  # mimics memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Your common settings: Below this line define 3rd party library settings
