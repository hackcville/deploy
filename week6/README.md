## Lightsail Deployment

### Setting up a production Docker environment

Add `.env.prod` to `.gitignore` to make sure you don't accidentally commit it.

Add `gunicorn==19.*` to your `requirements.txt`.

In `settings.py`, change the following lines:

```python
SECRET_KEY = os.environ.get("SECRET_KEY", "foo")

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "localhost 127.0.0.1 [::1]"
).split(" ")
```

Create a `docker-compose.prod.yml` with the following contents:

```yml
version: '3'

services:
  web:
    build: .
    command: gunicorn fridge_tracker.wsgi:application --bind 0.0.0.0:8000
    ports:
      - '80:8000'
    environment:
      - SQL_ENGINE=django.db.backends.postgresql
      - SQL_DATABASE=django_dev
      - SQL_USER=django
      - SQL_PASSWORD=django
      - SQL_HOST=db
      - SQL_PORT=5432
    env_file:
      - ./.env.prod
    depends_on:
      - db
  db:
    image: postgres:12.0-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=django
      - POSTGRES_PASSWORD=django
      - POSTGRES_DB=django_dev

volumes:
  postgres_data:
```

### Creating your instance

Go to [AWS Lightsail](https://aws.amazon.com/lightsail/). If you'd like some free student credit (this shouldn't be very expensive anyways), you can join [AWS Educate](https://www.awseducate.com/registration).

Select a blueprint > OS Only > Ubuntu 18.04 LTS.
The cheapest plan is fine (\$3.50 / month, free first month)

This will take a bit! Go grab a snack.

### Connecting to your instance

The easiest way is to SSH through your browser. Go to your instance dashboard > Connect > Connect using SSH.

Alternatively you can go to your instance dashboard > Connect > at the bottom of the page, "download your default private key from the Account page". Download your default SSH key. Put this somewhere safe on your computer and:

```
chmod 400 LightsailDefaultKey-us-east-1.pem
ssh -i LightsailDefaultKey-us-east-1.pem ubuntu@your_public_ip
```

Once you're in your instance, `git clone` your project - it doesn't matter where, but by default you'll

### Package setup

Run this in your instance to install Docker and Docker Compose:

```sh
# install docker
curl -sSL https://get.docker.com | sh

# install docker-compose
sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

# make docker-compose executable
chmod +x /usr/local/bin/docker-compose
```

### `.env.prod` configuration

Go into your project with `cd your_project_name`. Next, we need to create a `.env.prod` file in your instance. Since we don't have a graphical text editor, we'll have to use a terminal-based editor - we recommend `nano`. Run `nano .env.prod` and you'll have an editor open. Add the following contents:

```
SECRET_KEY=some_very_secret_key
DJANGO_ALLOWED_HOSTS=your_public_ip
```

To save your file, `Control + O` and `Enter`. To exit, `Control + X`.

If you'd like a simple way to create a secret key, you can try [this website](https://humberto.io/blog/tldr-generate-django-secret-key/). If the idea of having someone else generate a key for you is scary, try [this solution instead](https://humberto.io/blog/tldr-generate-django-secret-key/).

### Running your app

To tell Docker Compose we want to use our new `docker-compose.prod.yml`, run the following command:

```
sudo docker-compose -f docker-compose.prod.yml up
```

If all went well, you should be able to access your app through your public IP!

If you get an error of "Bad Request (400)" when visiting your app, you likely didn't configure your `DJANGO_ALLOWED_HOSTS` properly - make sure you set it to your public IP in `.env.prod`.

## Assignment submission

Deploy your fridge app! Slack us your public IP that we can use to view your app.
