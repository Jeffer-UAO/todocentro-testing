from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    verbose_name = '2. Administración de Pedidos'

    def ready(self):
            import orders.signals 
