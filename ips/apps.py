from django.apps import AppConfig


class IpsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ips'
    verbose_name = 'Control de Inventario'


    def ready(self):
            import ips.signals 
