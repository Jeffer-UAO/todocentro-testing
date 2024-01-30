from django.db import models
from django.db.models import Max


class Ip(models.Model):
    TIPO = [
        ('SALDOS INICIALES', 'EA'),
        ('ENTRADA', 'E1')
    ]

    cust = models.ForeignKey('custs.Tercero', on_delete=models.PROTECT, verbose_name="Proveedor")
    number = models.PositiveIntegerField(editable=False, default=0, verbose_name=u'No. Documento')
    tipo = models.CharField(max_length=20, choices=TIPO)
    total = models.DecimalField(max_digits=22, decimal_places=2, default=0.00)
    concept = models.CharField(max_length=80, verbose_name='Concepto', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Creado")

    class Meta:
        unique_together = ('number', 'tipo')
        verbose_name = "Entrada"
        verbose_name_plural = "Entrada de mercancía"

    def save(self, *args, **kwargs):
        try:
            if not self.pk:
                # Obtener el último número para el tipo actual
                ultimo_numero = Ip.objects.filter(tipo=self.tipo).aggregate(Max('number'))['number__max']

                # Incrementar en 1 si hay un último número, de lo contrario, comenzar desde 1
                nuevo_numero = ultimo_numero + 1 if ultimo_numero else 1

                # Actualizar el campo 'number' con el nuevo número
                self.number = nuevo_numero

            super(Ip, self).save(*args, **kwargs)

        except Exception as e:
            # Manejar la excepción y retornar un mensaje personalizado
            return f"No se pudo guardar la entrada. Error: {str(e)}"

    def __str__(self):
        return f"{self.tipo} No. {self.number}"
    

class Ipdet(models.Model):   
    ip = models.ForeignKey(Ip, on_delete=models.CASCADE)     
    item = models.ForeignKey('products.Product', on_delete=models.CASCADE ,verbose_name="Item")
    tipo = models.CharField(editable=False, max_length=20, null=True, blank=True)
    number = models.PositiveIntegerField(editable=False, default=0)
    qty = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False, default= 1, verbose_name=(u'Cantidad'))
    cost = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default= 0.0, verbose_name=(u'Costo'))
    subtotal = models.DecimalField(max_digits=22, decimal_places=2, blank=False, null=False, default= 0.0, verbose_name=(u'SubTotal'))
    comments = models.CharField(max_length=100, blank=True, verbose_name=(u'Comentario'))
        
    def save(self, *args, **kwargs):
        # Establecer tipo y número basándose en la propiedad ip_info
        self.tipo, self.number = self.ip.tipo, self.ip.number

        # Calcular el subtotal al multiplicar el costo por la cantidad
        self.subtotal = self.cost * self.qty
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Detalle"
        verbose_name_plural = "Detalles"

    def __str__(self):
        return f"{self.ip} - {self.item}"


