# Week 3: Intro to Django!

## Goals:

- Understand core Django concepts of models, views and templates
- Implement multiple pages which share a common base template
- Be able to interact with models using the Django shell
- Understand how to inject data into a template using page context

This week's assignment is meant to familiarize you with fundamental Django concepts. You'll notice that some of your tasks intentionally have very sparse instructions - this is meant to be practice for learning how to understand concepts using public documentation. The official Django docs are incredibly detailed and should be your go-to for any questions.

## Create a Django app

In order to add content to your project, you first need to create an app to hold it. As a reminder, a Django project can have many separate apps. To do this, we need to run a command inside of your `web` service container.

```
# Start your project if you haven't already
docker-compose up -d

# Open a bash shell inside of your web service
docker-compose exec web bash

# Once inside your container, create a new Django app
python manage.py startapp week2_app
```

In this case, we're only going to have one app so we can be a bit lazy and just call it `week2_app`. As we scale our projects, you'll want these names to be a bit more meaningful.

## Register your app

Open `week2/settings.py` and edit your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'week2_app.apps.Week2AppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

## Configure your views

In `week2/urls.py`, configure your router to send all requests to `week2_app`. Notice the additional import of `include`:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('week2_app.urls')),
    path('admin/', admin.site.urls),
]
```

Now, create a `week2_app/urls.py` with the following contents:

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index)
]
```

## Create a view and template

In `week2_app/views.py`, create a new `index` view:

```python
def index(request):
    return render(request, 'index.html')
```

We need to create the actual template for this view to render. Create a new file at `week2_app/templates/index.html` with any HTML content:

```html
<h1>This is our index template!</h1>
```

If all went well, you should see your index page successfully rendered at `localhost:8000`!

## Additional tasks

The above instructions should set up a baseline Django project. We'd also like you to complete some additional tasks as well:

- Implement at least two models (in `week2_app/models.py`) with some sort of relationship between them. Django has some great information on working with models in the [second part of their Django tutorial](https://docs.djangoproject.com/en/3.0/intro/tutorial02/).

- Create an additional view + template such as an about page (we aren't picky about the name / contents)

- Create a common template (such as `base.html`) that both `index.html` and your second template extend. [This article](https://tutorial.djangogirls.org/en/template_extending/) has some good information on how to accomplish that.

- After creating models and saving some data to your database, render it in one of your templates. The [third part of the Django tutorial](https://docs.djangoproject.com/en/3.0/intro/tutorial03/) has some info on how to do this in your view functions.

**We know this is a lot - try your best to work through as much as you can!** This project will extend into week 4 as well (with some minor additional tasks), but we expect as least some progress for this week. Being able to understand all of these concepts will be super important in the coming weeks as we create more complex Django apps.

## Submission requirements

- A link to your GitHub repo with all of your project code
- A screenshot of you interacting with your models in the Django shell (`python manage.py shell`)
- A screenshot of one of your templates displaying data from your models

We're available both in lab and any time on Slack to help answer your questions.
