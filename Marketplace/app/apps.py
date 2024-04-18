from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    
    def ready(self):
        # This will import your signals module when the app is ready
        import app.signals