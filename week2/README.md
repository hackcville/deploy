# Week 2: Getting Started with Docker and Django

## Goals:

- Understand the fundamentals of Docker and why we use containers
- Be able to create custom images using Dockerfiles
- Create a basic Django project and update a page with your own content

## Before Starting

Make sure you have Docker Desktop fully running! You'll be needing it throughout this assignment.

## Creating your custom image

Start by making a file called `Dockerfile` in a new project folder with the following contents:

```
FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
```

If you don't understand what this file is accomplishing, make sure to ask in lab! It's super important that you're aware of what Docker is doing behind the scenes.

Additionally, create a `requirements.txt` specifying that we need Django 3 in our project:

```
Django>=3.0
```

Next, we need to build our custom image so that can create containers based off of it. You can name your image anything, but this example uses `deploy-week2`. In a command line with its current directory set to your project folder:

```
docker build -t deploy-week2 .
```

The `.` tells Docker to try to find a Dockerfile in the current directory which we made earlier. If all goes well, you should see some output showing your image being built.

## Initializing your Django project

We need to run the command `django-admin startproject week2 .` in order to generate all necessary Django files for our project. However, we don't necessarily have Django on our local computer! To do this, we can utilize our image we just built as it has Django included.

```
docker run -it -v ~/Desktop/week2-example:/app deploy-week2 bash
```

A couple things to note:

- The `-it` flag is required when using any interactive command such as `bash`.

- The `-v` flag is used to bind some local volume on our computer (`~/Desktop/week2-example`) to one in our container (`/app`).

- The next argument specifies the image to use when making our container - in our case, `deploy-week2` which we just created earlier.

- The last argument is the command we want to execute in our new container - in our case, `bash` so we can have a shell to execute commands in inside our container.


Now, we can run the command to initialize the Django project.
```
django-admin startproject week2 .
```

If all went well, you should have a new folder called `week2` both inside your container and in your local project folder! You can exit your container using Control+D.

## Running our app

Here's an example of how we could start our app using vanilla Docker (don't do this quite yet):

```
docker run -it -v ~/Desktop/week2-example:/app deploy-week2 bash
root@ec54217e493c:/app# python manage.py runserver 0.0.0.0:8000
```

You should (hopefully) see some output showing that your Django server is running. However, if you try to visit http://localhost:8000, it won't work! This is because we haven't exposed any ports on our container to our local machine. We could do this by adding the flag `-p 8000:8000`, but...

You can begin to see how much of a hassle running Docker commands can be, especially if you're a new project contributor and don't know exactly how others are configuring their containers on their local machines. docker-compose is a super helpful tool that will solve this for us!

Create a `docker-compose.yml` in your project with the following contents:

```
version: '3'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - '8000:8000'
```

This is doing a couple of things:

- Defining a service for our app - in this case, one that runs Django. Later on we'll have multiple services in the same app.

- Specifying the Dockerfile to use for building. The `.` just means to look for it in the same directory.

- Defining the command to use when running our service. This is the same Django command we used earlier.

- Creating a volume mount between our local machine and our container. You can see we're allowed to use relative paths here with `.` - much nicer than having to list a whole path!

- Defining the port binding between our local machine and container. In this case, port 8000 in our container corresponds to port 8000 on our local machine.

We can now start our app just by running `docker-compose up`! You can immediately see how powerful this is in a team setting - there's no ambiguity on how to start working on a project.

Additionally, we can add the `-d` flag after our command to run our services in detached mode (in the background). To re-attach to the services and view their logs, run `docker-compose logs -f`.

Simiarly, to stop all of your running compose containers (in our case just one), run `docker-compose down`.

## Viewing your project

If everything worked as expected, you should be greeted with the following page at http://localhost:8000:

![](https://i.imgur.com/VSWwdBs.png)

Please try to reach this point before coming to this week's lab - in lab, we'll be going over how to make new Django apps and create actual content for your site.
