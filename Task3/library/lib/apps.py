# lib/apps.py
from django.apps import AppConfig

class LibConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lib'

    def ready(self):
        import lib.signals  # Ensure signals are registered
