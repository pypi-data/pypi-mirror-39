
# dcomputationaltool

Dcomputationaltool is a Django app which handle the genome coordinates 

Quick start
-----------

1. Add "dcomputationaltool" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dcomputationaltool',
    ]

2. Include the dcomputationaltool URLconf in your project urls.py like this::

    url(r'^dcomputationaltool/', include((dcomputationaltool.urls, 'dcomputationaltool'), namespace='dcomputationaltool')),

3. Run `python manage.py migrate` to create the dcomputationaltool models.

