"""
Production settings for {{cookiecutter.project_name}} project.

- Use WhiteNoise for serving static files{% if cookiecutter.use_s3 == 'y' %}
- Use Amazon's S3 for storing uploaded media{% endif %}{% if cookiecutter.use_mailgun == 'y' %}
- Use mailgun to send emails{% endif %}{% if cookiecutter.use_sentry_for_error_reporting == 'y' %}
- Use sentry for error logging{% endif %}
"""
{% if cookiecutter.use_sentry_for_error_reporting == 'y' %}import logging{% endif %}
from .base import *  # noqa
{%- if cookiecutter.use_sentry_for_error_reporting == 'y' %}
# raven sentry client
# See https://docs.sentry.io/clients/python/integrations/django/
INSTALLED_APPS += ['raven.contrib.django.raven_compat', ]{% endif %}

# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = envs("DJANGO_SECRET_KEY")

WHITENOISE_MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware', ]
MIDDLEWARE = WHITENOISE_MIDDLEWARE + MIDDLEWARE

{%- if cookiecutter.use_sentry_for_error_reporting == 'y' -%}
RAVEN_MIDDLEWARE = ['raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware']
MIDDLEWARE = RAVEN_MIDDLEWARE + MIDDLEWARE
{% endif %}

# SECURITY CONFIGURATION
# See https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#run-manage-py-check-deploy

# No need to set this HSTS stuff here, because Caddy is taking care of it.
# Look for Strict-Transport-Security in Caddyfile
# SECURE_HSTS_SECONDS = 518400
# SECURE_HSTS_INCLUDE_SUBDOMAINS = envs.as_bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
# Caddyfile: X-Content-Type-Options
# SECURE_CONTENT_TYPE_NOSNIFF = envs.as_bool('SECURE_CONTENT_TYPE_NOSNIFF', default=True)
# Caddyfile: X-Frame-Options
# X_FRAME_OPTIONS = 'DENY'
# Caddyfile: X-XSS-Protection
# SECURE_BROWSER_XSS_FILTER = True
# Using Caddy for this too
# SECURE_SSL_REDIRECT = envs.as_bool('SECURE_SSL_REDIRECT', default=True)
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# IMPORTANT: It's better to do this on the nginx / caddy
ALLOWED_HOSTS = envs.as_list('ALLOWED_HOSTS', default=['{{cookiecutter.domain_name}}'])

# http://gunicorn.org/
INSTALLED_APPS += ['gunicorn']
{% if cookiecutter.use_s3 == 'y' %}
# STORAGE CONFIGURATION
# Uploaded Media Files
# See: http://django-storages.readthedocs.io/en/latest/index.html
INSTALLED_APPS += ['storages']

AWS_ACCESS_KEY_ID = envs('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = envs('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = envs('AWS_STORAGE_BUCKET_NAME')
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = "public-read"

_AWS_EXPIRY = 60 * 60 * 24 * 7
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': f'max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate',
}

# URL that handles the media served from MEDIA_ROOT, used for managing
# stored files.
MEDIA_URL = f'https://s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
{% else %}
MEDIA_URL = '/media/'
{% endif %}
# Static Assets
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = Path(envs("HOMEAPP")) / Path("static-root/")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# EMAIL
DEFAULT_FROM_EMAIL = envs('DEFAULT_FROM_EMAIL', default='{{cookiecutter.django_project_name}} <noreply@{{cookiecutter.domain_name}}>')
EMAIL_SUBJECT_PREFIX = envs('EMAIL_SUBJECT_PREFIX', default='[{{cookiecutter.django_project_name}}]')
SERVER_EMAIL = envs('SERVER_EMAIL', default=DEFAULT_FROM_EMAIL){% if cookiecutter.use_mailgun == 'y' %}

# Anymail with Mailgun
# NOTE: you could use mailgun in development to keep close to the production configs
# just use the sandbox api key.
INSTALLED_APPS += ['anymail', ]
ANYMAIL = {
    'MAILGUN_API_KEY': envs('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': envs('MAILGUN_SENDER_DOMAIN')
}
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'{% endif %}

# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa F405
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]

# DATABASE CONFIGURATION
DATABASES["default"]["PASSWORD"] = envs("POSTGRES_PASSWORD")
{% if cookiecutter.use_sentry_for_error_reporting == 'y' %}
# Sentry Configuration
SENTRY_DSN = envs('DJANGO_SENTRY_DSN')
SENTRY_CLIENT = envs('DJANGO_SENTRY_CLIENT', default='raven.contrib.django.raven_compat.DjangoClient')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry', ],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console', ],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console', ],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console', ],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry', ],
            'propagate': False,
        },
    },
}
SENTRY_CELERY_LOGLEVEL = int(envs('DJANGO_SENTRY_LOG_LEVEL', logging.INFO))
RAVEN_CONFIG = {
    'CELERY_LOGLEVEL': int(envs('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)),
    'DSN': SENTRY_DSN
}
{% elif cookiecutter.use_sentry_for_error_reporting == 'n' %}
# LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', ],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', ],
            'level': 'ERROR',
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'mail_admins', ],
            'propagate': True
        }
    }
}
{% endif %}
# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # The default minimum is 8 characters
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # Set the length, example:
        # 'OPTIONS': {
        #     'min_length': 9,
        # }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Additional production stuff:
