FROM python:3.7-alpine3.9 AS base

ENV HOMEAPP=/django
ENV PROJECT_NAME={{cookiecutter.django_project_name}}
ENV PATH=$PATH:$HOMEAPP/.local/bin
ENV PYTHONPATH=$HOMEAPP:$PROJECT_NAME

# Python packages build dependencies
RUN apk add --no-cache --virtual .build-dependencies \
    # Essentials
    gcc musl-dev openssl-dev \
    # Postgres python client (psycopg2) build dependency
    postgresql-dev \
    # Pillow / PIL build dependencies
    freetype-dev jpeg-dev libwebp-dev tiff-dev libpng-dev lcms2-dev \
    openjpeg-dev zlib-dev libxslt-dev libxml2-dev libffi-dev \
    # Python packages run dependencies
    && apk add --no-cache \
    # Pillow / PIL
    freetype jpeg libwebp tiff libpng lcms2 openjpeg zlib libxslt libxml2 libffi \
    # Localization
    gettext \
    # Postgres python client
    libpq

WORKDIR $HOMEAPP/

# The other files will be added after installing the base packages
# This is to enforce caching layers
COPY ./requirements/base.txt ./requirements/base.txt

RUN pip install -r requirements/base.txt \
    && rm -R /root/.cache/pip \
    && apk del .build-dependencies

# Copy the rest of requirement files
# They should be installed in their own stages
COPY ./requirements/ ./requirements/

COPY manage.py ./

# Using a non-privileged user to own our code and things related to the project
RUN adduser -S -h $HOMEAPP django \
    # if you opt to use media-root/ and/or static-root
    # you should consider to use a volume
    # and in production beware of replicas and node placement
    # storage is a pain in distributed environment
    # that's why you probably be using S3 at least for media objects
    # but this can be useful locally
    && mkdir -p media-root/ static-root/ \
    && chown -R django:nogroup $HOMEAPP/


## PRODUCTION STAGE
FROM base AS production

USER django

ENV DJANGO_SETTINGS_MODULE=$PROJECT_NAME.config.production

ADD  --chown=django:nogroup https://raw.githubusercontent.com/douglasmiranda/lab/master/docker-secrets-as-env/docker-secrets-to-env-var.sh ./
COPY --chown=django:nogroup ./deployment/django/*.sh ./
RUN chmod +x django-entrypoint.sh

ENTRYPOINT ["/django/django-entrypoint.sh"]
# Our code
COPY --chown=django:nogroup ./$PROJECT_NAME $HOMEAPP/$PROJECT_NAME


## DEVELOPMENT STAGE: In this stage we'll be installing the dev dependencies, that's it.
# The code will be mounted as a volume so we can edit the code real time.
# In multi-stage builds you can choose to stop at a specific stage, that's what you will
# do in this case, stop at "DEV" stage. More info:
# https://docs.docker.com/develop/develop-images/multistage-build/#stop-at-a-specific-build-stage
# How to stop at a specific stage with Docker Compose:
# https://docs.docker.com/compose/compose-file/#target
FROM base AS development

ENV DJANGO_SETTINGS_MODULE=$PROJECT_NAME.config.local
# Since, I'm using only on dev I'll disable this
# So, do NEVER disable this if you deploy Werkzeug on production
ENV WERKZEUG_DEBUG_PIN=off
ENV PYTHONBREAKPOINT=ipdb.set_trace

RUN apk --no-cache add shadow
# Please inform this build arg, you can find your ID with `id -u $USER`
# https://github.com/douglasmiranda/lab/tree/master/docker-volume-share-user-host-container
ARG DJANGO_USER_UID=1000
RUN usermod -u ${DJANGO_USER_UID} django

USER django

RUN pip install --user --no-cache-dir -r requirements/dev.txt
# So you can remember to mount the code on your docker-compose.yml
# ./{{cookiecutter.django_project_name}}:/django/{{cookiecutter.django_project_name}}
VOLUME ["$HOMEAPP/$PROJECT_NAME"]
