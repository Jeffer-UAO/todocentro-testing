from django.apps import AppConfig


class WarehomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'warehome'
    verbose_name = ' Entrada y salida de Productos'

    def ready(self):
        from . import receivers
