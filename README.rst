Django Project Template
=======================

This is a template for Django Projects. Ready to run with Docker, with development and production settings.

Features
---------

* Django 2 + Python 3.6/3.7
* Using Alpine Linux based images (Wow, so lightweight :B)
* Setup close to production + nice dev tools when local
* Ready to use `Docker Secrets`_ for keeping you sensitive data safe
* Ready to use `Docker Configs`_ if you want
* Development:
  * Build and run with `Docker Compose`_
  * Django Extensions
  * Django Debug Toolbar
  * ipdb
  * Format code style with Black!
* Production:
  * Deploy with `Docker Compose`_ or `Docker Swarm`_ (`docker stack`_ command)
  * Run your Django using gunicorn
  * Reverse proxy with Caddy_ (easy HTTPS)
  * Serve static files with Whitenoise_
  * Media storage using Amazon S3
  * Redis for Cache and Session Storage
  * Send emails via Anymail_ (using Mailgun_ by default, but switchable)
* Bonus: Check the Makefile, you'll see lots of shortcuts to speed up your development

Optional Integrations
---------------------

*These features can be enabled during initial project setup.*

* Integration with MailHog_ for local email testing
* Integration with Sentry_ for error logging

.. _Mailgun: http://www.mailgun.com/
.. _Whitenoise: https://whitenoise.readthedocs.io/
.. _Anymail: https://github.com/anymail/django-anymail
.. _MailHog: https://github.com/mailhog/MailHog
.. _Sentry: https://sentry.io/welcome/
.. _Docker Configs: https://docs.docker.com/engine/swarm/configs/
.. _Docker Secrets: https://docs.docker.com/engine/swarm/secrets/
.. _Docker Compose: https://github.com/docker/compose
.. _Docker Swarm: https://docs.docker.com/engine/swarm/
.. _docker stack: https://docs.docker.com/engine/reference/commandline/stack/
.. _Caddy: https://caddyserver.com/
.. _LetsEncrypt: https://letsencrypt.org/

Usage
------

Let's pretend you want to create a Django project called "redditclone". Rather than using `startproject`
and then editing the results to include your name, email, and various configuration issues that always get forgotten until the worst possible moment, get cookiecutter_ to do all the work.

First, get Cookiecutter. Trust me, it's awesome::

    $ pip install "cookiecutter"

Now run it against this repo::

    $ cookiecutter https://github.com/douglasmiranda/ddpt

You'll be prompted for some values. Provide them, then a Django project will be created for you.

**Warning**: After this point, change 'Douglas', 'douglascoding', etc to your own information.

Answer the prompts with your own desired options_. For example::

    TODO

Enter the project and take a look around::

    $ cd reddit/
    $ ls

Create a git repo and push it there::

    $ git init
    $ git add .
    $ git commit -m "first awesome commit"
    $ git remote add origin git@github.com:YOURGITHUBUSERNAME/redditclone.git
    $ git push -u origin master

Submit a Pull Request
~~~~~~~~~~~~~~~~~~~~~~

Keep your pull requests small. Better yet, explain what you plan to do in the issues, it will save time in the end.

Credits
-------

Powered by Cookiecutter_, Cookiecutter Django is my template for Django projects.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`douglasmiranda/ddpt`: https://github.com/douglasmiranda/ddpt
