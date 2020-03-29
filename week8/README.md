# Testing + Continuous Integration!

Writing new code is great, but it's also important to make sure it still works! Creating meaningful tests can help you both keep your project stable and give you some guidance throughout development. In a team environment for your final projects, it may be easy for bugs to creep in, so tests can help keep things in check.

Let's start by writing some basic tests!

## Creating tests in Django

In any of your app directories (such as `core`), create a a `tests.py` if it doesn't already exist. Your file will have the following basic form:

```py
from django.test import TestCase


class SomeTestCase(TestCase):
    # An optional function that will run before every test
    # Can be useful to create some dummy model data
    def setUp(self):
        # ...

    # All test methods must begin with test
    def test_some_thing(self):
        # some app logic
        self.assertTrue(some_condition)

```

For example, here are some basic tests for our fridge tracker:

```py
from django.test import TestCase
from .models import Item
from django.contrib.auth.models import User


class ItemTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='james', password='very_secure')
        Item.objects.create(name='Eggs', owner=user)
        Item.objects.create(name='Cheese', owner=user)

    def test_number_of_items(self):
        print(Item.objects.all())
        self.assertEqual(Item.objects.all().count(), 2)

    def test_item_str_representation(self):
        eggs = Item.objects.get(name='Eggs')
        cheese = Item.objects.get(name='Cheese')

        self.assertEqual(str(eggs), 'Eggs')
        self.assertEqual(str(cheese), 'Cheese')
```

These tests are a bit mundane, but understanding this structure is key for developing useful tests in your own app.

To run your tests:

```bash
docker-compose exec web python manage.py test
```

If anything goes wrong, you should see a detailed output of what happened.

Behind the scenes, Django is creating entirely new database tables in PostgreSQL (or whatever db you're using) prefixed with `test` to give us an isolated environment. Once the tests are completed, it tears them down.

## Continuous Integration

These tests are nice, but how can I be sure my group member will actually remember to run tests manually when they make changes? Luckily, continuous integration (or CI) helps us out here. By frequently running tests as our code develops (say, on every new commit or on a new pull request), we can keep track of any new bugs easily and pinpoint exactly where they begin.

To setup our CI pipeline, we're going to be using a free service called GitHub Actions, built right into GitHub. The platform allows us to define various "workflows" that can be automatically run by GitHub when certain events occur. These workflows can also perform just about anything and are useful for way more than just CI testing.

To get started, let's create a new file in our project called `.github/workflows/continuous-integration.yml` (the actual file name is arbitrary, though the path is not). Give it the following contents:

```yml
name: Continuous Integration

on: [push, pull_request]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v1
      - name: Run Docker Compose services
        run: |
          docker-compose up -d
      - name: Wait for Django start
        run: |
          while ! nc -z localhost 8000; do
            sleep 0.1
          done
      - name: Run Django Tests
        run: |
          docker-compose exec -T web python manage.py test
```

Whoa, lots of text. Let's break this down:

- We start by giving our workflow a name and use the `on` keyword to define when our task is run. GitHub provides lots of flexibility for this - check out the [docs page](https://help.github.com/en/actions/configuring-and-managing-workflows/configuring-a-workflow) for more info.

- Next, we define our job called `ci` and state that we're running it with an Ubuntu container. That's right - we're running our tests inside of a container that GitHub will spin up for us! Our Docker knowledge is already coming in handy.

- We can now define a sequence of steps to execute in order to complete our workflow. The first one is fairly simple and just clones our repository into the new container.

- Next, we run our services with Docker Compose just as we've been doing in development. Note that while the previous step used a premade action (`actions/checkout@v1`), this step just executes a custom command that we specify. In running this step, Docker Compose will also need to build our images since it will be our first time running in this container.

- Before we can continue with tests, we need to make sure Django has fully started since it can sometimes take a few seconds to finish up. We're performing a similar check to what we did in `entrypoint.sh` for our PostgreSQL setup where we continuously check for an active port (in this case 8000) until we connect.

- Finally, we actually run the tests! This just uses the same command as above with the addition of `-T` which is [needed in order to run in this environment](https://github.com/docker/compose/issues/5696#issuecomment-425126228).

Whew! That was a lot, but in theory you should be able to use this directly without any issues. Just push this file up to GitHub and any future commits / pull requests should be tested! Here's an example pull request where the CI workflow was automatically run (and passed!):

![](https://i.imgur.com/jKN28g4.png)

If you click on Details for any workflow, you can see the full execution logs (even in realtime!):

![](https://i.imgur.com/xY3AIms.png)

## Assignment Submission

Write some tests for one of your apps (such as the fridge tracker) and add a CI workflow! For your submission, send us a link to one of your workflow details pages (such as the one above) so we can see that all of your tests passed.
