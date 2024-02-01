from django.apps import AppConfig


class BillsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bills'
    verbose_name = 'Administración de Factura'

    # def ready(self):
    #         import orders.signals 