#!/bin/sh

set -o errexit
set -o pipefail

source $HOMEAPP/docker-secrets-to-env-var.sh

if [[ "${DJANGO_SETTINGS_MODULE}" == "${PROJECT_NAME}.config.production" ]]; then
    python $HOMEAPP/manage.py check --deploy
    python $HOMEAPP/manage.py collectstatic --noinput
fi

exec "$@"
