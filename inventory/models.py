from django.db import models
from customers.models import Client
from django_tenants.utils import get_public_schema_name, schema_exists, get_tenant_model

class Itemact(models.Model):   
    ipdet = models.ForeignKey('receipts.Ipdet', on_delete=models.CASCADE, null=True, blank=True, default=None)        
    orderdet = models.ForeignKey('orders.Orderdet', on_delete=models.CASCADE, null=True, blank=True, default=None)        
    oedet = models.ForeignKey('bills.Oedet', on_delete=models.CASCADE, null=True, blank=True, default=None)        
    item = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    qty = models.DecimalField(max_digits=9, decimal_places=2, default= 0)
    tipo = models.CharField(editable=False, max_length=20, null=True, blank=True)
    number = models.PositiveIntegerField(editable=False, default=0)

    class Meta:
        verbose_name = "Itemact"
        verbose_name_plural = "Itemacts"

    def __str__(self):
        return str(self.ipdet)


class ItemactItem(models.Model):   
    tenant = models.ForeignKey('customers.Client', on_delete=models.CASCADE, blank=True, default="", null=True)
    item = models.ForeignKey('products.Product', on_delete=models.CASCADE, null=True, blank=True, default="")
    cantidad_actual = models.DecimalField(max_digits=9, decimal_places=2, default= 0)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    uuid = models.UUIDField(editable=False, blank=True, null=True)
    images = models.CharField(max_length=600, default="", blank=True)
    image_alterna = models.CharField(max_length=600, default="", blank=True)
    description = models.TextField(max_length=2000, blank=True, default="")
    price1 = models.DecimalField(max_digits=12, decimal_places=2, default= 0.0)
    price2 = models.DecimalField(max_digits=12, decimal_places=2, default= 0.0)
    price_old = models.DecimalField(max_digits=12, decimal_places=2, default= 0.0)
    flag = models.CharField(max_length=200, blank=True, default="")
    ref = models.CharField(max_length=200, blank=True, default="")
    qty = models.DecimalField(max_digits=9, decimal_places=2, default= 0.0)
    slug = models.CharField(max_length=200, blank=True, default="")
    active = models.CharField(max_length=5, blank=True, default="")
    soldout = models.CharField(max_length=5, blank=True, default="")
    offer = models.CharField(max_length=5, blank=True, default="")
    home = models.CharField(max_length=5, blank=True, default="")

    class Meta:
        verbose_name = "Administración de Entrada"
        verbose_name_plural = "Administración de Entradas"

    
    def __str__(self):
        return f"{self.item} - {self.nombre}"
    
  