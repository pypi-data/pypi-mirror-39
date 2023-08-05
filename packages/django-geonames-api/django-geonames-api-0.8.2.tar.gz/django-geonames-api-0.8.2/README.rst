===============
django-geonames
===============

django-geonames is a simple Django app to implement the geonames database in
your Django application. (load a contry from geonames, have the geographic
autocompletion)

No detailed documentation is available for the time being.

Quick start
-----------

1. Add "django-geonames" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'geography',
        ...
    ]

2. Run `python manage.py migrate` to create the geonames models.

How to test?
------------

python runtests.py --settings test_settings
