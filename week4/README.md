# Week 3: Forms and PostgreSQL!

## Goals:

- Be able to implement forms in Django to give clients a way to interact with models

- Replace sqlite with a more robust PostgreSQL database

- Implement more than one service with Docker Compose

## Forms

[Django's documentation](https://docs.djangoproject.com/en/3.0/topics/forms/) has some excellent information on how to get started with forms. We've also included some samples in [this week's slides](https://docs.google.com/presentation/d/1-brEJMY128Njp1MO53vw6Ky636-fSaqzbCubfCwhovw), though they may not make much sense out of context.

We'd like you to implement a form (or multiple depending on your model setup) so that your users can create new data entries from your app. These don't have to look good yet! Just focus on functionality for now.

## PostgreSQL

Convert your project's sqlite-based configuration to use PostgreSQL instead. This will require an additional service in your `docker-compose.yml` as well as some other changes - for an in-depth breakdown, view the [django-postgres-starter README](django-postgres-starter/README.md).

## Submission requirements

Please complete all tasks listed in [week3](../week3/README.md) as well as the above tasks. Before week 5's workshop, please submit the following via Slack:

- A link to your shared GitHub repo with all of your project code
- A screenshot of you interacting with your models in the Django shell (`python manage.py shell`)
- Screenshots showing existing data rendered in a template and a usable form

Only one group member needs to submit, but please mention who you worked with!
