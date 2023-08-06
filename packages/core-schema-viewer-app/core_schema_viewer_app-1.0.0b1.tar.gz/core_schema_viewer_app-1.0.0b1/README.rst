======================
Core Schema Viewer App
======================

Schema Viewer feature for the curator core project.


Configuration
=============

1. Add "core_schema_viewer_app" to your INSTALLED_APPS setting like this
------------------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
        ...
        "core_schema_viewer_app",
    ]


2. Include the core_schema_viewer_app URLconf in your project urls.py like this
-------------------------------------------------------------------------------

.. code:: python

    url(r'^', include("core_schema_viewer_app.urls")),


3. Oxygen configuration
-----------------------

- For *production* environment, follow the steps described in Oxygen.prod.README.rst
- For *development* environment, follow the steps described in Oxygen.dev.README.rst
