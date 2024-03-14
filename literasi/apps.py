from django.apps import AppConfig


class LiterasiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'literasi'
    
    def ready(self):
        import literasi.signals
