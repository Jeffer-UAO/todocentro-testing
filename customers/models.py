from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Customer(models.Model):
    DOCUMENT = (
        ('CEDULA', 'C.C'),
        ('TARGETA DE IDENTIDAD', 'T.I'),
        ('NIT', 'Nit')
    )

    id_n = models.CharField(
        primary_key=True, max_length=20, editable=True, verbose_name=(u'No. Documento'))
    tipo = models.CharField(
        max_length=20, verbose_name=(u'Tipo de documento'), choices=DOCUMENT, default='Auto')
    email = models.CharField(
        max_length=150, verbose_name=(u'Correo electrónico'), blank='True', null='True')
    company = models.CharField(
        max_length=100, verbose_name=(u'Razon social'))
    address = models.CharField(max_length=100, verbose_name=(
        u'Dirección'), blank='True', null='True')
    phone = models.CharField(max_length=100, verbose_name=(
        u'Teléfono'), blank='True', null='True')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tercero'
        verbose_name_plural = 'Terceros'

    def __str__(self):
        return self.company


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True


class Domain(DomainMixin):
    pass
