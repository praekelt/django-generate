Django Generate
===============
**Django slightly smarter than fixtures content generation app.**

``django-generate`` adds a management command called ``generate`` which allows you to create objects from a JSON description of said objects. The objects will only be created once via Django's ``get_or_create`` method. Inheritance base model objects are created where needed. File fields can also be populated from arbitrary resources. In this way ``django-generate`` simplifies generating complex objects when compared to `Django's builtin fixtures feature <https://docs.djangoproject.com/en/dev/howto/initial-data/#providing-initial-data-with-fixtures>`_. 

.. contents:: Contents
    :depth: 5

This package is part of the larger `Jmbo <http://www.jmbo.org>`_ project.

Installation
------------

#. Install or add ``django-generate`` to your Python path.

#. Add ``generate`` to your ``INSTALLED_APPS`` setting.

Usage
-----

