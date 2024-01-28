from django.db import models

class Tercero(models.Model):    
    name = models.CharField(max_length=20, verbose_name=(u'Nombre'))
    document = models.IntegerField(verbose_name='Nit')  # TODO: validar que sea un DNI o CUIT válido
    addres = models.TextField(blank=True, verbose_name='Dirección')
    phone = models.CharField(max_length=15, blank=True, verbose_name='Teléfono')
    email = models.EmailField(blank=True, verbose_name='Correo')
    cust = models.BooleanField(default=True, verbose_name='Proveedor')
    

    class Meta:
        verbose_name = "Tercero"
        verbose_name_plural = "Terceros"

    def __str__(self):
        return str(self.name)