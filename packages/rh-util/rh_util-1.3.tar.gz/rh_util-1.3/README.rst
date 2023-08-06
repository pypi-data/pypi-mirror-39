=====
RH_Util
=====

RH_Util is a simple Django application containing support libraries for HR projects.


Quick start
-----------

1. Add "rh_util" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rh_util',
    ]

2. Include the rh_util URLconf in your project urls.py like this::

    path('rh_util/', include('rh_util.urls')),

3. Run `python manage.py migrate` to create the rh_util models.


