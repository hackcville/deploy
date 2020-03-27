# Fixtures

As you start working with your new group, you may find it difficut to debug issues that your group members are running into. For example (thinking back to the fridge tracker), what if your group member added cheese to their fridge in a particular way that you can't replicate on your end? What if you both just want a consistent set of test data you can share?

Fixtures aim to solve this by storing SQL data as a file (likely in JSON) which can be shared between collaborators through version control and loaded later on. Note that this is _not_ a replacement for a database - rather, it just helps provide some initial seed data for our database to use.

With our app running, we can run the `dumpdata` command to collect all of our app's data. The `>` symbol is used to redirect the output of `dumpdata` into a file - in this case, `core/fixtures/initial_data.json` (be sure to change this depending on your app name).

```bash
docker-compose exec web python manage.py dumpdata > core/fixtures/initial_data.json
```

Next, let's try wiping our database just to demonstrate how fixtures work:

```bash
docker-compose exec web python manage.py flush
```

If we use our app, we'll see there's no data! Let's load our fixtures back in:

```bash
docker-compose exec web python manage.py loaddata initial_data.json
```

Django will automatically look through all of your installed apps' `fixture` folders for valid files to load - in our case, `initial_data.json`. If all went well, you should see your data back in your app!
