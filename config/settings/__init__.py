"""Settings package — auto-selects module from DJANGO_SETTINGS_MODULE env var.

By default, uses ``config.settings.dev``. Set ``DJANGO_SETTINGS_MODULE``
environment variable to switch:

    DJANGO_SETTINGS_MODULE=config.settings.prod
    DJANGO_SETTINGS_MODULE=config.settings.test
"""
