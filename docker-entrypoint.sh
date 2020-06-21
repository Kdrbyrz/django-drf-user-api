#!/bin/bash

if [ "$SQL_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

set -euxo pipefail

python manage.py migrate

python manage.py loaddata users

python manage.py collectstatic --no-input --clear

exec "$@"
