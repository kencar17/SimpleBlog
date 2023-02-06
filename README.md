<p align="center">
  <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/kencar17/SimpleBlog?color=blue"/>
  <img alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"/>
  <img alt="Pylint" src="https://img.shields.io/badge/linting-pylint-yellowgreen"/>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-red.svg" alt="License">
  </a>
</p>

# Simple Blog

Simple Blog made with Django

## Features

Simple Blog provides the following features:

Authentication:
- JWT Authentication

## To-dos

Authentication:
- [x] ~~JWT Authentication~~
- [ ] User Management Endpoint
- [ ] Password Reset Endpoint
- [ ] Oauth Auth?
- [ ] MFA (Text, Email, Authenticator App)
- [ ] Account or User

Account:
- [X] ~~Account~~
- [ ] Account Followers
- [ ] Account Following

Blog:
- [ ] Blog Management Endpoint
- [ ] Tie Blog to User or Account
- [ ] Comments
- [ ] Categories
- [ ] Tags

Notifications:
- [ ] Push Notifications
- [ ] Email Notifications
- [ ] Text Notification

Other:
- [X] Secret Key Generation

## Getting Started

You can get started with Simple Blog immediately on the Amplication Cloud. 

Alternatively you can set up a local development environment.

Environment Variables
- BLOG_SECRET_KEY (random chars)
- BLOG_SIGNING_KEY (random chars)

```bash
# Clone Report to local
git clone git@github.com:kencar17/SimpleBlog.git

# Create Virtual Environment or Environment of your choice
python -m venv venv

# Install Project Requirements
pip install -r requirements.txt

# Create BLOG_SECRET_KEY and BLOG_SIGNING_KEY. Make sure to copy theses as Environment Variables
# Optional param: --secret_key' - Specify length of key, defaults to 50
# Optional param: --signing_key' - Specify length of key, defaults to 50
python manage.py generate_secret_keys

# Make Migrations and Migrate Django Project
python manage.py makemigrations
python manage.py migrate

# Create Superuser
python manage.py createsuperuser

# Run Project
python manage.py runserver
```

In browser of your choice, navigate to http://localhost:8000/

Note: Please ensure all environment variables are configured

# Contributing

Simple Blog is an open-source project. We are committed to a fully transparent development process and highly appreciate any contributions. Whether you are helping us fix bugs, proposing new features, improving our documentation or spreading the word - we would love to have you as a part of the Simple Blog community.
