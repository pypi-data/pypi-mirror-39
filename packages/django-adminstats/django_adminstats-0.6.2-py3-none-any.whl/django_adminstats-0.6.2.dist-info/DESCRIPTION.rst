==================
Django Admin Stats
==================

|pipeline-badge| |coverage-badge| |pypi-badge|

Django Admin Stats allows you to create and display charts of your data
using the django admin. It uses `c3 <https://c3js.org/>`_ to display charts.

Features
--------

* Supports generating statistics from django models and from trackstats_
  metrics.
* Also allows for custom statistics generation by making your own
  ``Registration`` subclass.
* Nice JavaScript charts with c3, falls back to a plain table without
  JavaScript.
* Add filters & group data by setting query parameters on the criteria

Limitations
-----------

* One dimension/axis of the chart is always the date. There's no way to
  specify a chart that isn’t “by date”.

Installation
------------

Installation is straightforward. Install ``django-adminstats`` with pip, and
then add ``'django_adminstats',`` to your ``INSTALLED_APPS`` setting.

Registering Statistics
----------------------

In order to do anything, you'll need register some models or trackstats
metrics. You can find examples of this in ``tests/models.py``, but the short
of it looks like this:

.. code-block:: python

   from django_adminstats.registry import register_model

   class Currency(models.Model):
       slug = models.CharField(max_length=10)
       name = models.CharField(max_length=100)
       current_usd_rate = models.DecimalField()
       sign = models.CharField(max_length=10, default='$')

   class Transaction(models.Model):
       amount = models.DecimalField()
       currency = models.Foreignkey(to=Currency)
       date = models.DateTimeField(auto_now_add=True)

   register_model(Transaction)


By default, we look for a field called ‘date’ on the model, and it should be
either a ``DateField`` or ``DateTimeField``. If you want to use a different,
field (for example if you’re using Django’s default user and you want to chart
by ‘joined_at’) you need to create a registration subclass.

.. code-block:: python

   from django_adminstats.registry import registry, register

   class UserRegistration(ModelRegistration):
       date_field = 'joined_at'

   register(UserRegistration())


Creating Charts
---------------

You can add charts in the admin. In order for the chart to show anything, you
need to add criteria. By default, it will just show a count of all the items
charted by the date field, if you to change this, you need to add things in
the filter query, axis query, and group query fields.

First, the content of these fields is formatted like a URL querystring,
for example a filter query of ``message=Hello%20World&x=y`` is equivalent to
``.filter(message='Hello World', x='y')``. Note that you only use the
``key0=value0&key1=value1`` form in the filter query, the axis and group
queries are just ``key0&key2``.

Second, you can use lookups and relations just like in a normal django
query (e.g. ``field__gt=2`` or ``field__related_field``).

Finally, you can also specify functions to use on the field by doing
``field:function``. For example ``id:count`` is the default axis query when
the field is left blank.


Demo
----

Just run ``make demo`` and log in with user ``admin`` and password ``admin``.


.. |pipeline-badge| image:: https://gitlab.com/alantrick/django-adminstats/badges/master/pipeline.svg
   :target: https://gitlab.com/alantrick/django-adminstats/
   :alt: Build Status

.. |coverage-badge| image:: https://gitlab.com/alantrick/django-adminstats/badges/master/coverage.svg
   :target: https://gitlab.com/alantrick/django-adminstats/
   :alt: Coverage Status

.. |pypi-badge| image:: https://img.shields.io/pypi/v/django_adminstats.svg
   :target: https://pypi.org/project/django-adminstats/
   :alt: Project on PyPI

.. _trackstats: https://pypi.org/project/django-trackstats/



