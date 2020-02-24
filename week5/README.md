# Week 5: User Authentication!

## Goals:

- Be able to restrict content based on a user's authentication state
- Use a User as a model field to associate data with specific users
- Manage users within the Django admin dashboard

## Assignment details

Design a fridge app!

- Users can view current fridge items and (if authenticated) add their own items
- For each item in the fridge, keep track of information such as (but not limited to) name, date + time entered, an an opitonal expiration date
- Implement user authentication so that only logged in users can add items
- Keep track of the user that added something and list their info alongside the item

Some technical requirements:

- Django + Docker (duh)
- A PostgreSQL database to hold your data (see [django-postgres-starter](../week4/django-postgres-starter/README.md))
- Functional login / signup pages to manage authentication (see [django-auth-starter](./django-auth-starter/README.md))

Some things that would be nice to implement:

- Make it look nice! We want you to have fun with this assignment, so take some time to style your templates with style libraries such as Bulma or Bootstrap.
- If you'd really like to go above and beyond, try implementing an interactive date/time picker like I demoed in class! I used [flatpickr](https://flatpickr.js.org/) but you're welcome to use any library.

## Presentations

We will be doing (very brief) presentation again, so be ready to have your project ready to share! Like last time, these are super informal and shouldn't require any preparation, but just be sure everyone in your group is able to explain how your app works.

## Submission requirements

- A link to your shared GitHub repo with all of your project code
- A screenshot of your page(s) showing core functionality

Only one group member needs to submit, but please mention who you worked with!
