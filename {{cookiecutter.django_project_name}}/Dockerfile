FROM python:3.7-alpine3.9 AS builder

# Build dependencies
RUN apk add --no-cache \
    # Essentials
    gcc musl-dev openssl-dev \
    # Postgres python client (psycopg2) build dependency
    postgresql-dev \
    # Pillow / PIL build dependencies
    freetype-dev jpeg-dev libwebp-dev tiff-dev libpng-dev lcms2-dev \
    openjpeg-dev zlib-dev libxslt-dev libxml2-dev libffi-dev

WORKDIR /requirements/
COPY ./requirements/ ./
# By doing this, the packages will be pre-compiled
# which is nice for docker multi-stage builds
RUN pip wheel --pre --wheel-dir=./ -r dev.txt


## SETUP STAGE: In this stage we'll just define the basics of our environment.
FROM python:3.7-alpine3.9 AS setup

ENV HOMEAPP=/django
ENV PROJECT_NAME={{cookiecutter.django_project_name}}
ENV PATH=$PATH:$HOMEAPP/.local/bin
ENV PYTHONPATH=$HOMEAPP:$PROJECT_NAME

RUN addgroup -S django && adduser -h $HOMEAPP -S -G django django \
    && apk add --no-cache \
    # Pillow / PIL
    freetype jpeg libwebp tiff libpng lcms2 openjpeg zlib libxslt libxml2 libffi \
    # Postgres python client
    libpq

WORKDIR $HOMEAPP/
# Our Python Packages + requirements files
COPY --from=builder /requirements/ r/
ADD https://raw.githubusercontent.com/douglasmiranda/lab/master/docker-secrets-as-env/docker-secrets-to-env-var.sh ./docker-secrets-to-env-var.sh

COPY ./entrypoint.sh ./
COPY manage.py ./

RUN chown -R django:django ./
# Using a non-privileged user to own our code and things related to the project
USER django
ENTRYPOINT ["/django/entrypoint.sh"]


## DEVELOPMENT STAGE: In this stage we'll be installing the dev dependencies, that's it.
# The code will be mounted as a volume so we can edit the code real time.
# In multi-stage builds you can choose to stop at a specific stage, that's what you will
# do in this case, stop at "DEV" stage. More info:
# https://docs.docker.com/develop/develop-images/multistage-build/#stop-at-a-specific-build-stage
# How to stop at a specific stage with Docker Compose:
# https://docs.docker.com/compose/compose-file/#target
FROM setup AS development

ENV DJANGO_SETTINGS_MODULE=$PROJECT_NAME.config.local
# Since, I'm using only on dev I'll disable this
# So, do NEVER disable this if you deploy Werkzeug on production
ENV WERKZEUG_DEBUG_PIN=off
ENV PYTHONBREAKPOINT=ipdb.set_trace

# So you can remember to mount the code on your docker-compose.yml
# ./{{cookiecutter.django_project_name}}:/django/{{cookiecutter.django_project_name}}
VOLUME ["$HOMEAPP/$PROJECT_NAME"]

RUN pip install --pre --user --no-index --only-binary=:all: --find-links=r/ -r r/dev.txt


## PRODUCTION STAGE
FROM setup AS production

ENV DJANGO_SETTINGS_MODULE=$PROJECT_NAME.config.production

RUN pip install --pre --user --no-index --only-binary=:all: --find-links=r/ -r r/base.txt \
    && rm -R $HOMEAPP/r/

COPY --chown=django:django ./deployment/healthchecks.sh ./
# Our code
COPY --chown=django:django ./$PROJECT_NAME $HOMEAPP/$PROJECT_NAME
