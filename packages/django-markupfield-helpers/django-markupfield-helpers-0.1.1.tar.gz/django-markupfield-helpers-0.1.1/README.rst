**************************
django-markupfield-helpers
**************************

``django-markupfield-helpers`` is a set of Django helpers that make it easier to get up and running quickly with ``django-markupfield``.

Source code is available on GitHub at `mfcovington/django-markupfield-helpers <https://github.com/mfcovington/django-markupfield-helpers>`_. Information about ``django-markupfield`` is available on `GitHub <https://github.com/jamesturk/django-markupfield>`_.


.. contents:: :local:


Installation
============

**PyPI**

.. code-block:: sh

    pip install django-markupfield-helpers


**GitHub (development branch)**

.. code-block:: sh

    pip install git+http://github.com/mfcovington/django-markupfield-helpers.git@develop


Configuration
=============

Add ``markupfield_helpers`` to ``INSTALLED_APPS`` in ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'markupfield_helpers',
    )


Add a link to the CSS file for syntax highlighting in ``base.html`` or in a specific template.

.. code-block:: python

    {% load staticfiles %}

    <link rel="stylesheet" type="text/css" href="{% static 'markupfield_helpers/css/syntax-highlighting.css' %}">


``markupfield_helpers`` can be left out of ``INSTALLED_APPS`` if the provided CSS for syntax highlighting is not needed.


Helpers
=======

``MarkupField``
---------------

The ``MarkupField`` class from ``markupfield_helpers`` can be used in place of the class of the same name from ``markupfield``.

The ``markupfield_helpers`` version comes with four markup types defined:

- ``Markdown`` (**Default**): Markdown 2 with extras (``code-friendly``, ``cuddled-lists``, ``fenced-code-blocks``, ``footnotes``, and ``tables``)
- ``Markdown Basic``: Markdown 2 without extras
- ``Plain Text``
- ``reStructuredText``


Here is a basic example of how to use the ``markupfield_helpers`` version of ``MarkupField``:

.. code-block:: python

    from django.db import models
    from markupfield_helpers.helpers import MarkupField

    class Article(models.Model):
        title = models.CharField(max_length=100)
        slug = models.SlugField(max_length=100)
        body = MarkupField()


``MARKUP_FIELD_TYPES``
----------------------

Alternatively, ``MARKUP_FIELD_TYPES`` can be imported from ``markupfield_helpers.helpers`` and used as-is or modified.
This is equivalent to the code above:


.. code-block:: python

    from django.db import models
    from markupfield.fields import MarkupField
    from markupfield_helpers.helpers import MARKUP_FIELD_TYPES


    class Article(models.Model):
        title = models.CharField(max_length=100)
        slug = models.SlugField(max_length=100)
        body = MarkupField(
            default_markup_type='Markdown',
            markup_choices=MARKUP_FIELD_TYPES,
        )


Issues
======

If you experience any problems or would like to request a feature, please `create an issue <https://github.com/mfcovington/django-markupfield-helpers/issues>`_ on GitHub.


*Version 0.1.1*
