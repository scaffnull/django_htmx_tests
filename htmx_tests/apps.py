from django.apps import AppConfig


class HtmxTestsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'htmx_tests'

    # Add car to carpool when created
    def ready(self):
        from . import signals