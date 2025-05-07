from django.apps import AppConfig


class TallerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Taller'

    def ready(self):
        import Taller.signals  # 👈 Esto importa las señales al iniciar
