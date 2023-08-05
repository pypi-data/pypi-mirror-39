=============================
Pyfb-normalization
=============================

.. image:: https://badge.fury.io/py/pyfb-normalization.svg
    :target: https://badge.fury.io/py/pyfb-normalization

.. image:: https://travis-ci.org/mwolff44/pyfb-normalization.svg?branch=master
    :target: https://travis-ci.org/mwolff44/pyfb-normalization

.. image:: https://codecov.io/gh/mwolff44/pyfb-normalization/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mwolff44/pyfb-normalization

Normalization application package. TRansform phone number to E.164 numbers. Mainly used in PyFreeBilling project.

Documentation
-------------

The full documentation is at https://pyfb-normalization.readthedocs.io.

Quickstart
----------

Install pyfb-normalization::

    pip install pyfb-normalization

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'pyfb_normalization.apps.PyfbNormalizationConfig',
        ...
    )

Add pyfb-normalization's URL patterns:

.. code-block:: python

    from pyfb_normalization import urls as pyfb_normalization_urls


    urlpatterns = [
        ...
        url(r'^', include(pyfb_normalization_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
