# Django PostgreSQL Starter

This project should be a good starting point for any Dockerized Django apps using PostgreSQL. The Django server runs from the `web` service while PostgreSQL runs from `db`.

**Please read through this whole file before using! It's very important that you understand what's going on.**

To use this starter:

```bash
git clone https://github.com/hackcville/deploy
# copy week4/django-postgres-starter to somewhere on your computer
# or just run right from the cloned deploy folder
cd deploy/week4/django-postgres-starter

# if you run into any permissions errors while running your web container, try this first:
chmod +x entrypoint.sh

docker-compose up
```

## `settings.py` changes

If you were to start from a fresh Django project rather than using the example `deploy_project`, make the following changes:

```python
# ...

DEBUG = int(os.environ.get("DEBUG", default=0))

# ...

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}
```

This configures the debug and database settings to read from environment variables that we pass in through `docker-compose.yml`. In theory you could hardcode these values, but it's better to leave these flexible; in the future, we may configure a different SQL database such as AWS RDS.

## `postgres_data` volume

Even if our `db` container gets destroyed, we want the database contents to remain accessible. In our previous setup with sqlite, this wasn't an issue since `db.sqlite3` remained on our local computer - any changes made in the container were reflected in our local file due to the service's volume bind mount (`.:/app`).

We could have a similar setup with PostgreSQL - the database's data lives in `/var/lib/postgresql/data/` inside the `db` container, so we could set up a volume bind mapping such as `./db:/var/lib/postgresql/data/`. However, we don't really need to keep the data files inside our project folder since they aren't readable anyways.

Luckily, Docker provides a better alternative for us: [volumes](https://docs.docker.com/storage/volumes/). Rather than managing a folder for the data ourselves, we can instead store it in a Docker volume. This is essentially a special filesystem managed by Docker that has lots of advantages - view the docs page linked if you're curious.

To set this up, we can use a similar volume mount syntax of `postgres_data:/var/lib/postgresql/data`. Note that the left-hand argument is just `postgres_data` (our volume name) rather than a relative path beginning with a dot.

We also need to define the volume at the bottom of the compose file:

```yml
volumes:
  postgres_data:
```

You can view all Docker volumes on your machine with `docker volume ls`. If the volume is not in use by a container, you can remove it with `docker volume rm`. Additionally, you can `docker-compose down -v` to remove any linked volumes in addition to service containers.

## `entrypoint.sh`

You may notice a new file `entrypoint.sh` in the project directory. This is necessary to ensure that the Django doesn't start before PostgreSQL is ready. Though the `web` service won't start until `db` has started (due to the `depends_on` option in `docker-compse.yml`), this doesn't necessarily guarantee that PostgreSQL is ready - it may still take a few seconds until the database server has completely started.

To fix this, we can define an "entrypoint" which runs before any command is executed in our `web` container. In this case, the script waits for the PostgreSQL server to be actively accepting connections before continuing. We can setup the entrypoint with the following line in our `Dockerfile`:

```dockerfile
ENTRYPOINT ["./entrypoint.sh"]
```

## Other notes

- The base image in the `Dockerfile` is now `python:3.8.0-alpine` - this is required so that we can use `apk` to install packages for PostgreSQL.

- We also need to include the `psycopg2-binary` library in `requirements.txt` so that Django can communicate with our PostgreSQL server.

- The database options like `SQL_USER` are arbitrary - as long as they match between the `web` and `db` environment variables, you can choose anything. We don't care about making these secure since the database isn't accessible from outside of Docker.

- You may also notice that migrations are automatically run when the `web` service starts. This is because `python manage.py migrate` is included in `entrypoint.sh` - this isn't required but is definitely more convenient than having to run migrations manually.

- If you try to `docker-compose exec web bash`, you may notice that you get an error. This is because Alpine Linux (what our `web` service is based on) doesn't include bash by default. Instead, use `docker-compose exec web ash`.
