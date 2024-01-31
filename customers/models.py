from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
import uuid


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


class Product_public(models.Model):
    item = models.UUIDField(editable=False, blank=True, null=True)
    codigo = models.CharField(
        max_length=50, verbose_name=("Código")
    )   
    name_extend = models.CharField(
        max_length=200, unique=True, verbose_name=("Nombre Producto")
    )
    images =  models.CharField(
        max_length=600, null=True, default="", blank=True, verbose_name=("Imagen")
    )
    image_alterna = models.CharField(
        max_length=600, null=True, default="", blank=True, verbose_name=("Imagen Alterna")
    )
    description = models.TextField(
        max_length=2000, blank=True, verbose_name=("Descripción el producto")
    )
    price1 = models.PositiveIntegerField(
        blank=True, null=True, default=0, verbose_name=("Precio Detal")
    )
    price2 = models.PositiveIntegerField(
        blank=True, null=True, default=0, verbose_name=("Precio por Mayor")
    )
    price_old = models.PositiveIntegerField(
        blank=True, null=True, default=0, verbose_name=("Precio Anterior")
    )
    flag = models.CharField(
        max_length=200, blank=True, null=True, default="", verbose_name=("Grupo")
    )
    ref = models.CharField(
        max_length=200, blank=True, null=True, default="", verbose_name=("Referencia")
    )   
    slug = models.SlugField(max_length=200, unique=True, verbose_name=("Url"))
    published_public = models.BooleanField(default=True, verbose_name=("Publicado"))
    published = models.BooleanField(default=True, verbose_name=("Local"))
    active = models.BooleanField(default=True, verbose_name=("Activo"))
    soldout = models.BooleanField(default=False, verbose_name=("Agotado"))
    offer = models.BooleanField(default=False, verbose_name=("Oferta"))
    home = models.BooleanField(default=False, verbose_name=("Exclusivo"))
    created_date = models.CharField(
        max_length=50, blank=True, null=True, default="", verbose_name=("Creado")
    )
    modified_date = models.CharField(
        max_length=50, blank=True, null=True, default="", verbose_name=("Modificado")
    )
    domain = models.CharField(max_length=255, blank=True, null=True)
   
   # Meta data for SEO and Open Graph protocols    
    def __str__(self):
        return f"{self.codigo} - {self.name_extend}"
   

 