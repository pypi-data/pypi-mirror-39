easy_jsonfield
==============

A semi-private fork of `jsonfield2`_(, which is a modern fork of `django-jsonfield`_, compatible with the latest versions of Django).

.. _jsonfield2: https://github.com/rpkilby/jsonfield2/
.. _django-jsonfield: https://github.com/dmkoch/django-jsonfield/

-----

**easy_jsonfield** is a reusable model field that allows you to store validated JSON, automatically handling
serialization to and from the database. To use, add ``easy_jsonfield.JSONField`` to one of your models.

**Note:** `django.contrib.postgres`_ now supports PostgreSQL's jsonb type, which includes extended querying
capabilities. If you're an end user of PostgreSQL and want full-featured JSON support, then it is
recommended that you use the built-in JSONField. However, jsonfield2 is still useful when your app
needs to be database-agnostic, or when the built-in JSONField's extended querying is not being leveraged.
e.g., a configuration field.

.. _django.contrib.postgres: https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#jsonfield


Requirements
------------

jsonfield2 aims to support all current `versions of Django`_, however the explicity tested versions are:

* **Python:** 3.4, 3.5, 3.6, 3.7
* **Django:** 1.11, 2.0, 2.1

.. _versions of Django: https://www.djangoproject.com/download/#supported-versions


Installation
------------

.. code-block:: python

    pip install easy_jsonfield


Usage
-----

.. code-block:: python

    from django.db import models
    from easy_jsonfield import JSONField

    class MyModel(models.Model):
        json = JSONField()


Advanced Usage
--------------

By default python deserializes json into dict objects. This behavior differs from the standard json
behavior  because python dicts do not have ordered keys. To overcome this limitation and keep the
sort order of OrderedDict keys the deserialisation can be adjusted on model initialisation:

.. code-block:: python

    import collections

    class MyModel(models.Model):
        json = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})


Other Fields
------------

**easy_jsonfield.JSONCharField**

Subclasses **models.CharField** instead of **models.TextField**.


Running the tests
-----------------

The test suite requires ``tox`` and ``tox-venv``.

.. code-block:: shell

    $ pip install tox tox-venv


To test against all supported versions of Django, install and run ``tox``:

.. code-block:: shell

    $ tox

Or, to test just one version (for example Django 2.0 on Python 3.6):

.. code-block:: shell

    $ tox -e py36-django20


Release Process
---------------

* Update changelog
* Update package version in setup.py
* Create git tag for version
* Upload release to PyPI

.. code-block:: shell

    $ pip install -U pip setuptools wheel
    $ rm -rf dist/ build/
    $ python setup.py bdist_wheel upload


Changes
-------

Take a look at the `changelog`_.

.. _changelog: https://github.com/claydodo/easy_jsonfield/blob/master/CHANGES.rst
