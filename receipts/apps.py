from django.apps import AppConfig


class IpsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'receipts'
    verbose_name = 'Administración de Entradas'


    def ready(self):
            import receipts.signals 
