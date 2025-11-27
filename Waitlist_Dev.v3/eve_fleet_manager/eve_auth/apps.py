from django.apps import AppConfig

class EveAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eve_auth'

    def ready(self):
        # Signals removed as we are using a direct view callback approach
        pass