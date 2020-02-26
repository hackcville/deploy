#!/bin/sh

# Only run the database check if we're set to PostgreSQL
if [ "$SQL_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Waiting for PostgreSQL..."

    # Checking if the database is actively accepting connections
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Running migrations on container start
python manage.py migrate

# Executing original command (likely starting Django)
exec "$@"