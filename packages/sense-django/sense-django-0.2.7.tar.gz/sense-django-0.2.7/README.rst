============
sense-django
============

sense-django is a simple Django app. It contains three middlewares used in django project.  

Quick start
-----------

1. Add "sense_django" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'sense_django',
    ]

2. Add "sense_django.middleware.UserTokenCheck" to your MIDDLEWARE settings like this::

    MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
    'sense_django.middleware.UserTokenCheck',
    'sense_django.middleware.PermissionCheck',
    'sense_django.middleware.RequestLogMiddleware'
    ]
