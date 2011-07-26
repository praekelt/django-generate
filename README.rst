Django Generate
===============
**Django slightly smarter than fixtures content generation app.**

``django-generate`` adds a management command called ``generate`` which allows you to create objects from a dynamically created JSON description of said objects. It's primary focus is to generate test content for use during project development and testing. Objects are only created once via Django's ``get_or_create`` method. Inheritance base model objects are created where needed. File fields can also be populated from arbitrary resources. In this way ``django-generate`` simplifies generating complex objects when compared to `Django's built in fixtures feature <https://docs.djangoproject.com/en/dev/howto/initial-data/#providing-initial-data-with-fixtures>`_. 

.. contents:: Contents
    :depth: 5

This package is part of the larger `Jmbo <http://www.jmbo.org>`_ project.

Installation
------------

#. Install or add ``django-generate`` to your Python path.

#. Add ``generate`` to your ``INSTALLED_APPS`` setting.

Usage
-----

In order to generate content you need to execute the ``generate`` management command. This command will search for a ``generator`` module in each of the apps as specified in the ``INSTALLED_APPS`` setting and call its ``generate`` method. This method should return a list of JSON serialized objects to be created.

**Note**: Generation is also triggered after a ``syncdb``, at which time you will be prompted to generate default content. If you answer yes to the prompt content will be generated in the same way is if you had run the ``generate`` command manually. 

As an example lets create 5 dummy users for testing.

1. Create a ``generator.py`` in the app you want to generate content's path.

2. Make sure your app is specified in your ``INSTALLED_APPS`` setting. Also make sure your app has a ``models.py`` so Django installs it correctly.

3. Edit the ``generator.py`` file to look like this::

    def generate():
        objects = []
        for i in range(1, 6):
            objects.append({
                "model": "auth.User",
                "fields": {
                    "username": "user_%s" % i,
                    "first_name": "User %s Name" % i,
                    "is_staff": True,
                },
            })
        return objects

All this is really doing is generating a bunch of JSON serialized objects dynamically. The returned ``objects`` list looks like this::
    
    [{'fields': {'username': 'user_1', 'first_name': 'User 1 Name', 'is_staff': True}, 'model': 'auth.User'}, {'fields': {'username': 'user_2', 'first_name': 'User 2 Name', 'is_staff': True}, 'model': 'auth.User'}, {'fields': {'username': 'user_3', 'first_name': 'User 3 Name', 'is_staff': True}, 'model': 'auth.User'}, {'fields': {'username': 'user_4', 'first_name': 'User 4 Name', 'is_staff': True}, 'model': 'auth.User'}, {'fields': {'username': 'user_5', 'first_name': 'User 5 Name', 'is_staff': True}, 'model': 'auth.User'}]

This is a normal Django JSON fixtures list of objects that will be created. You could just as easily have hard coded and returned this list instead of generating it. The point is that the ``generate`` method should return a list of JSON serialized objects to be created.

4. Run the generate management command to generate the objects::
    
    $ python manage.py generate
    
After the command completes you should have 5 newly created staff users in your database. If you were to run the generate command again no new users would be created as ``django-generate`` detects the presence of previously generated objects.

Have a look at `jmbo-post's generator <https://github.com/praekelt/jmbo-post/blob/master/post/generator.py>`_ to see how objects with inheritance structures, relations and file resources can be created very easily using ``django-generate``.

