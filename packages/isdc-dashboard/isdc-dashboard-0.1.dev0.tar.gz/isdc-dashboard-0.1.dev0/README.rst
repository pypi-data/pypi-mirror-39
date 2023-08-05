=====
dashboard
=====

Process base mapping data used by other modules.
Mandatory Module for ASDC

Quick start
-----------

1. Add "dashboard" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dashboard',
    ]

    If necessary add "dashboard" in (check comment for description): 
        DASHBOARD_PAGE_MODULES, 
        GETRISKEXECUTEEXTERNAL_MODULES, 
        QUICKOVERVIEW_MODULES, 
        MAP_APPS_TO_DB_CUSTOM

    For development in virtualenv add GEODB_PARENT_DIR path to VENV_NAME/bin/activate:
        export PYTHONPATH=${PYTHONPATH}:\
        ${HOME}/GEODB_PARENT_DIR

2. Include the dashboard URLconf in geonode/urls.py like this::

    url('', include('dashboard.urls')),

3. Run `python manage.py migrate dashboard` to create the dashboard models.

