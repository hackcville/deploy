# Django Auth Starter

This project should be a good starting point for implementing user authentication into your Django project. All authentication is contained in the `user_auth` app, so you should be able to drop it into a project and get it working with some mild configuration.

If you'd like to configure auth on your own, instructions are below. However, if you'd like to use this starter as-is:

```bash
git clone https://github.com/hackcville/deploy
cd deploy
# or if you already have the deploy repo cloned:
cd deploy
git pull

# copy week5/django-auth-starter to somewhere on your computer
# or just run right from the cloned deploy folder
cd week5/django-auth-starter

docker-compose up
# run migrations!
docker-compose exec web python manage.py migrate
```

## Adding to your project

This README will assume you have a working Django project. In our case, we have a project called `auth_example` and an app called `core`.

Like mentioned above, all of the auth logic lives inside the `user_auth` app. Start by copying that folder into your root project folder.

Next, we need to register the app in our project. In `auth_example` (or whatever your project folder is called), edit `settings.py`:

```diff
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
+   'user_auth.apps.UserAuthConfig'
]
```

We also need to set some auth configuration flags - these will be useful later. You can add these to the bottom of `settings.py`:

```python
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login'
```

Next, we need to configure our project's `urls.py` to forward any auth requests to our `user_auth` app:

```diff
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
+   path('accounts/', include('user_auth.urls')),
    path('admin/', admin.site.urls)
]
```

Finally, we probably want to set some of our app's views to be restricted (only accessible to authenticated users). In `core/views.py`:

```diff
from django.shortcuts import render
+from django.contrib.auth.decorators import login_required


+@login_required
def index(request):
    return render(request, 'index.html')


+@login_required
def about(request):
    return render(request, 'about.html')
```

You should now be able to navigate to an authenticated route (or `/accounts/login`) and view the login page! You probably won't have any users created yet, so click "Create an account" and make some to test with. These are saved in your SQL database alongside your models.

## Project structure

It's super important that you understand the structure of this starter before you implement it into your own app!

```
├── auth_example (our Django project)
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── user_auth (app just used for auth functionality)
│   ├── apps.py
│   ├── templates
│   │   └── registration
│   │       ├── login.html
│   │       └── signup.html
│   ├── urls.py
│   └── views.py
├── core (our actual content app)
│   ├── apps.py
│   ├── templates
│   │   ├── about.html
│   │   ├── base.html
│   │   └── index.html
│   ├── urls.py
│   └── views.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── db.sqlite3
```
