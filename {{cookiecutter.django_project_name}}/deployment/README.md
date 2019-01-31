# Deployment

Before You Deploy Things
Before you start deploying you'll probably need to create some secrets.
For example: openssl rand -base64 20 | docker secret create POSTGRES_PASSWORD -
or: openssl rand -base64 50 | docker secret create DJANGO_SECRET_KEY -
