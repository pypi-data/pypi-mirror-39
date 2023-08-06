=============================
pyfb-routing
=============================

.. image:: https://badge.fury.io/py/pyfb-routing.svg
    :target: https://badge.fury.io/py/pyfb-routing

.. image:: https://travis-ci.org/mwolff44/pyfb-routing.svg?branch=master
    :target: https://travis-ci.org/mwolff44/pyfb-routing

.. image:: https://codecov.io/gh/mwolff44/pyfb-routing/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mwolff44/pyfb-routing

Routing package for PyFreeBilling application

Documentation
-------------

The full documentation is at https://pyfb-routing.readthedocs.io.

Quickstart
----------

Install pyfb-routing::

    pip install pyfb-routing

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'pyfb_routing.apps.PyfbRoutingConfig',
        ...
    )

Add pyfb-routing's URL patterns:

.. code-block:: python

    from pyfb_routing import urls as pyfb_routing_urls


    urlpatterns = [
        ...
        url(r'^', include(pyfb_routing_urls)),
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
