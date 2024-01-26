from django.db import models



class Ip(models.Model):
    TIPO = (
        ('SALDOS INICIALES', 'EA'),
        ('ENTRADA', 'E1')
    )

    number = models.PositiveIntegerField(editable=False, default=0, verbose_name=(u'No. Documento'))
    tipo = models.CharField(max_length=20, choices=TIPO)
    # cust = models.ForeignKey('custs.Tercero', on_delete=models.PROTECT, verbose_name=("Proveedor"))
    concept = models.CharField(max_length=80, verbose_name='Concepto', null=True, blank=True)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=("Creado"))


    class Meta:
        unique_together = ('number', 'tipo')
        verbose_name = "Entrada"
        verbose_name_plural = "Entrada de mercancia"

    def save(self, *args, **kwargs):
        try:
            # Verificamos si es una instancia nueva
            if not self.pk:
                # Obtenemos el último número para el tipo actual
                ultimo_numero = Ip.objects.filter(tipo=self.tipo).order_by('-number').first()

                # Si hay un último número, incrementamos en 1, de lo contrario, comenzamos desde 1
                nuevo_numero = int(ultimo_numero.number) + 1 if ultimo_numero else 1

                # Actualizamos el campo 'number' con el nuevo número
                self.number = str(nuevo_numero)               

            super(Ip, self).save(*args, **kwargs)

        except Exception as e:
            # Manejar la excepción y retornar un mensaje personalizado
            return f"No se pudo guardar la entrada. Error: {str(e)}"
    
    def __str__(self):
        return f"{self.tipo} No. {self.number}"
    

class Ipdet(models.Model):   
    tipo = models.CharField(editable=False, max_length=20, null=True, blank=True)
    number = models.PositiveIntegerField(editable=False, default=0)
    ip = models.ForeignKey(Ip, on_delete=models.CASCADE)     
    item = models.ForeignKey('products.Product', on_delete=models.CASCADE ,verbose_name="Item")
    qty = models.PositiveSmallIntegerField(default=1, verbose_name=(u'Cantidad'))
    cost = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False, default= 0.0, verbose_name=(u'Costo'))
    subtotal = models.DecimalField(max_digits=9, decimal_places
                                 =2, blank=False, null=False, default= 0.0, verbose_name=(u'SubTotal'))
    comments = models.CharField(
        max_length=100, blank=True, verbose_name=(u'Comentario'))
    
    
    @property
    def ip_info(self):
        # Acceder al tipo y número de la Ip relacionada
        return {'tipo': self.ip.tipo, 'number': self.ip.number}
    
    def save(self, *args, **kwargs):
        # Antes de guardar, establecer tipo y número basándose en la propiedad ip_info
        ip_info = self.ip_info
        self.tipo = ip_info['tipo']
        self.number = ip_info['number']

        # Calcular el subtotal al multiplicar el costo por la cantidad
        self.subtotal = self.cost * self.qty
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Detalle"
        verbose_name_plural = "Detalles"

    def __str__(self):
        return f"{self.ip} - {self.product}"


class Itemact(models.Model):   
    ipdet = models.ForeignKey(Ipdet, on_delete=models.CASCADE)        
    qty = models.PositiveSmallIntegerField(default=0)
    tipo = models.CharField(editable=False, max_length=20, null=True, blank=True)
    number = models.PositiveIntegerField(editable=False, default=0)
    item = models.ForeignKey('products.Product', on_delete=models.CASCADE)


    def __str__(self):
        return str(self.ipdet)


class ItemactItem(models.Model):
    itemact = models.OneToOneField(Itemact, on_delete=models.CASCADE, unique=True)
    item = models.ForeignKey('products.Product', on_delete=models.CASCADE, null=True, blank=True)
    cantidad_actual = models.PositiveIntegerField(default=0)
    nombre = models.CharField(max_length=200, blank=True, null=True)