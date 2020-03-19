# Week 7: Cloud databases!

So far, we've been relying on either a local `db.sqlite3` file or our `db` Docker service for our database needs. Let's change that and move our data to the cloud!

Lightsail offers an integrated database service that makes it easy for our existing app instances to talk to configured databases. Let's set up a new PostgreSQL isntance for our fridge tracker.

## Creating our database

Head to the [databases section of Lightsail](https://lightsail.aws.amazon.com/ls/webapp/home/databases) and click "Create database". You should see lots of options - we only care about changing a few:

- Be sure to select PostgreSQL as your database type. We could use MySQL, but our app is already configured with PostgreSQL drivers so we'll stick with that for now.

- We recommend choosing the cheapest plan (\$15 / month). Your first month should be free + if you set up [AWS Educate](https://aws.amazon.com/education/awseducate/), you should have lots of free credits to use if you go beyond that.

- Name your database something descriptive like `fridge-tracker-postgres`.

The initial setup may take a bit - go grab a drink!

## Testing our database connection

To make sure our database is running properly, let's try connecting to it with TablePlus. There's one catch here: by default, our PostgreSQL instance will only accept connections from Lightsail instances, not outside origins (like our local computer). Let's fix that!

Click on your database instance and go to the Networking tab. Enable public mode (might take a bit) so that we can connect. Next, go back to the Connect tab to grab your connection details.

We suggest using TablePlus but any SQL client should work to test this. Fill in the following connection details:

- Host/Socket: this is your instance endpoint (a super long URL near the top of the dashboard)

- Port: can leave empty since PostgreSQL always runs on 5432

- User: `dbmasteruser`

- Password: click on "show" next to the password section to reveal your unique password

- Database: `postgres` (the default database Lightsail creates for us)

Your connection should look like this:

![](https://i.imgur.com/hXMFQzf.png)

If you click on Test and your fields are all green, you're good to go! Try connecting and you should see an empty database with no tables yet.

## Configuring our app

Now that we know the database is working, we only need to make minimal changes to our Django app to tell it how to connect to this new database. As far as our app is concerned, this is just another PostgreSQL instance to connect to, so we only need to change our connection settings.

Since we won't be using a local PostgreSQL server in our Docker environment, let's change that in our `docker-compose.prod.yml`:

```diff
version: '3'

services:
  web:
    build: .
    command: gunicorn fridge_tracker.wsgi:application --bind 0.0.0.0:8000
    ports:
      - '80:8000'
-    environment:
-      - SQL_ENGINE=django.db.backends.postgresql
-      - SQL_DATABASE=django_dev
-      - SQL_USER=django
-      - SQL_PASSWORD=django
-      - SQL_HOST=db
-      - SQL_PORT=5432
    env_file:
      - ./.env.prod
-    depends_on:
-      - db
-  db:
-    image: postgres:12.0-alpine
-    volumes:
-      - postgres_data:/var/lib/postgresql/data
-    environment:
-      - POSTGRES_USER=django
-      - POSTGRES_PASSWORD=django
-      - POSTGRES_DB=django_dev

-volumes:
-  postgres_data:
```

Go ahead and commit + push those changes up to GitHub.

Back in our Lightsail instance (connect through SSH), we need to make some more changes. Before we do anything, it's probably a good idea to `sudo docker-compose stop` so that we don't mess anything up for potential live users while we do maintenance.

In our `.env.prod`, let's add back the database options we removed from our Compose file:

```diff
SECRET_KEY=some_very_secret_key
DJANGO_ALLOWED_HOSTS=your_public_ip

+SQL_ENGINE=django.db.backends.postgresql
+SQL_DATABASE=postgres
+SQL_USER=dbmasteruser
+SQL_PASSWORD=your_db_password
+SQL_HOST=your_db_host
+SQL_PORT=5432
```

If we just `sudo docker-compose start`, you'll notice that your existing data still shows in your app. This is because Docker hasn't picked up our new Compose file or environment variable changes - let's change that!

Remove everything (containers + your db volume) with `sudo docker-compose down -v` and recreate your `web` container with the previous startup command of `sudo docker-compose -f docker-compose.prod.yml up` (you may want to `-d` so that you can continue working in your shell).

If all went correctly, you should see migrations be applied (since we're working with a fresh database) and Gunicorn should start your app! Go to your app through its public IP and you should see a clean slate with no data. You can also refresh TablePlus and you should see all of your Django tables created.

## Final steps

Once you're done testing, we recommend turning off public mode so that you don't leave any security vulnerabilities open - you wouldn't want someone hacking your fridge!

If you wanted to keep your data in the midst of this migration, AWS has a helpful article on the topic: [Importing data into your PostgreSQL database in Amazon Lightsail](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-importing-data-into-your-postgres-database)

## Assignment submission

Take a screenshot of your Lightsail database dashboard and resend the public IP of your app so we can test it!
