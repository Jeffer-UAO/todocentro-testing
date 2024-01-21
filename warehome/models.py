from django.db import models
from customers.models import Customer
from accounts.models import Account
from products.models import Product, Attribut
from simple_history.models import HistoricalRecords
#from .signals import signal_warehomedetail


# ---------------------------------------------------------------

class RoutableModel(models.Model):
    ip_address = models.GenericIPAddressField('IP address', null=True)

    class Meta:
        abstract = True


class DocumentEntry(models.Model):
    type = models.CharField(max_length=2, unique=True,
                            verbose_name=(u'Tipo'))
    description = models.CharField(max_length=50,
                                   verbose_name=(u'Descripción'))

    class Meta:
        verbose_name = 'Tipo de Entrada'
        verbose_name_plural = 'Tipos de Entradas'

    def __str__(self):
        return str(self.type)


class DocumentOut(models.Model):
    type = models.CharField(max_length=2, unique=True,
                            verbose_name=(u'Tipo'))
    description = models.CharField(max_length=50,
                                   verbose_name=(u'Descripción'))

    class Meta:
        verbose_name = 'Tipo de Salida'
        verbose_name_plural = 'Tipos de Salidas'

    def __str__(self):
        return str(self.type)


class ProductEntry(models.Model):
    type = models.ForeignKey(
        DocumentEntry, on_delete=models.CASCADE, verbose_name=(u'Tipo'), default='E1')
    number = models.CharField(
        max_length=50, unique=True, verbose_name=(u'Factura No.'))
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name=(u'Proveedor'))
    created_date = models.DateField(
        verbose_name=(u'Creado'))
    deudate = models.DateField(
        verbose_name=(u'Vencimiento'))
    created_date_sistem = models.DateTimeField(
        auto_now_add=True)
    modified_date = models.DateTimeField(
        auto_now=True, verbose_name=(u'Modificado'))
    comments = models.CharField(
        max_length=100, blank=True, verbose_name=(u'Comentarios'))
    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self):
        return str(self.number)


class ProductOut(models.Model):
    type = models.ForeignKey(
        DocumentOut, on_delete=models.CASCADE, verbose_name=(u'Tipo'), default='P1')
    number = models.BigAutoField(primary_key=True,
                                 unique=True, verbose_name=(u'Documento No.'))
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name=(u'Cliente'))
    created_date = models.DateField(
        verbose_name=(u'Creado'))
    deudate = models.DateField(
        verbose_name=(u'Vencimiento'))
    created_date_sistem = models.DateTimeField(
        auto_now_add=True)
    modified_date = models.DateTimeField(
        auto_now=True, verbose_name=(u'Modificado'))
    comments = models.CharField(
        max_length=100, blank=True, verbose_name=(u'Comentarios'))
    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = 'Salida'
        verbose_name_plural = 'Salidas'

    def __str__(self):
        return str(self.number)


class WarehomeDetail(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=(u'Producto'))
    attribut = models.ForeignKey(   
        Attribut, on_delete=models.CASCADE, verbose_name=(u'Atributo'))
    description = models.CharField(
        max_length=15, blank=True, null=True, verbose_name=(u'Descripción'))
    qty = models.PositiveSmallIntegerField(
        verbose_name=(u'Cantidad'))
    costo = models.PositiveSmallIntegerField(
        verbose_name=(u'Costo unitario'))
    iva = models.PositiveSmallIntegerField(
        default=19, verbose_name=(u"Iva"))
    ProductEntry = models.ForeignKey(
        ProductEntry, on_delete=models.CASCADE, verbose_name=(u'-'), null=True, blank=True)
    ProductOut = models.ForeignKey(
        ProductOut, on_delete=models.CASCADE, verbose_name=(u'-'), null=True, blank=True)

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventario'
        #unique_together = ['product', 'qty']

    def __str__(self):
        #    signal_warehomedetail.send(sender=self.__class__, product=self.product, qty=self.qty, id_entry=self.ProductEntry, id_out=self.ProductOut)
        return str(self.product)


class Stock(models.Model):   
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=(u'Producto'))    
    qty = models.PositiveSmallIntegerField(
        verbose_name=(u'Cantidad'), editable=False)   
    attribut = models.ForeignKey(   
        Attribut, on_delete=models.CASCADE, verbose_name=(u'Atributo'))
    description = models.CharField(
        max_length=15, blank=True, null=True, verbose_name=(u'Descripción'))

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stock'

    def __str__(self):
        return str(self.product)

    