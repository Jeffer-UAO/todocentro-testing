from django.db import models


class Company(models.Model):
    id_n = models.CharField(
        primary_key=True, max_length=20, editable=True, verbose_name=(u'Nit'))
    email = models.CharField(
        max_length=150, verbose_name=(u'Correo electrónico'), blank='True', null='True')
    company = models.CharField(
        max_length=100, verbose_name=(u'Razon social'))
    web = models.CharField(
        max_length=100, verbose_name=(u'Página web'), blank='True', null='True')
    address = models.CharField(max_length=100, verbose_name=(
        u'Dirección'), blank='True', null='True')
    phone = models.CharField(max_length=100, verbose_name=(
        u'Teléfono'), blank='True', null='True')
    whatsaap = models.CharField(max_length=15, verbose_name=(
        u'WhatsApp'), blank='True', null='True')
    we = models.TextField(max_length=750, verbose_name=(
        u'Nosotros'), blank='True', null='True')   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Compañia'
        verbose_name_plural = 'Compañia'

    def __str__(self):
        return self.company
