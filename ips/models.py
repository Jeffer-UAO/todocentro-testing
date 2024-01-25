from django.db import models


class Ip(models.Model):
    TIPO = (
        ('SALDOS INICIALES', 'EA'),
        ('ENTRADAS', 'E1')
    )

    number = models.CharField(editable=False, max_length=20, verbose_name=(u'No. Documento'))
    tipo = models.CharField(max_length=20, choices=TIPO)
    # cust = models.ForeignKey('custs.Tercero', on_delete=models.PROTECT, verbose_name=("Proveedor"))
    concept = models.CharField(max_length=80, verbose_name='Concepto', null=True, blank=True)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=("Creado"))


    class Meta:
        unique_together = ('number', 'tipo')

    def save(self, *args, **kwargs):
        # Verificamos si es una instancia nueva
        if not self.pk:
            # Obtenemos el último número para el tipo actual
            ultimo_numero = Ip.objects.filter(tipo=self.tipo).order_by('-number').first()

            # Si hay un último número, incrementamos en 1, de lo contrario, comenzamos desde 1
            nuevo_numero = int(ultimo_numero.number) + 1 if ultimo_numero else 1

            # Actualizamos el campo 'number' con el nuevo número
            self.number = str(nuevo_numero)

        super(Ip, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"

    def __str__(self):
        return f"{self.number} - {self.tipo}"
    

class Ipdet(models.Model):   
    ip = models.ForeignKey(Ip, on_delete=models.CASCADE)     
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT ,verbose_name="Nombre")
    qty = models.PositiveIntegerField(default=1, verbose_name=(u'Cantidad'))
    cost = models.DecimalField(max_digits=9, decimal_places
                                 =2, blank=False, null=False, default= 0.0, verbose_name=(u'Costo'))
    subtotal = models.DecimalField(max_digits=9, decimal_places
                                 =2, blank=False, null=False, default= 0.0, verbose_name=(u'SubTotal'))
    comments = models.CharField(
        max_length=100, blank=True, verbose_name=(u'Comentario'))
    
    
    @property
    def ip_number(self):
        # Acceder al número de la Ip relacionada
        return self.ip.pk
    
    class Meta:
        verbose_name = "Detalle"
        verbose_name_plural = "Detalles"

    def __str__(self):
        return str(self.ip)