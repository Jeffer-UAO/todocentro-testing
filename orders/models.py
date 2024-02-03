from django.db import models
from django.db.models import Max



class Order(models.Model):
    TIPO = (
        ('PEDIDO INTERNO', 'PI'),
        ('PEDIDO EXTERNO', 'PE')
    )

    cust = models.ForeignKey('custs.Tercero', on_delete=models.PROTECT, verbose_name=("Cliente"))
    number = models.PositiveIntegerField(editable=False, default=0, verbose_name=(u'Pedido'))
    tipo = models.CharField(max_length=20, choices=TIPO, default= "PEDIDO INTERNO")
    total = models.DecimalField(max_digits=22, decimal_places=2, default=0.00)
    concept = models.CharField(max_length=80, verbose_name='Concepto', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=("Solicitado"))


    class Meta:
        unique_together = ('number', 'tipo')
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def save(self, *args, **kwargs):
        try:
            # Verificamos si es una instancia nueva
            if not self.pk:
                # Obtenemos el último número para el tipo actual                
                ultimo_numero = Order.objects.filter(tipo=self.tipo).aggregate(Max('number'))['number__max']

                # Si hay un último número, incrementamos en 1, de lo contrario, comenzamos desde 1
                nuevo_numero = ultimo_numero + 1 if ultimo_numero else 1

                # Actualizamos el campo 'number' con el nuevo número
                self.number = nuevo_numero

            super(Order, self).save(*args, **kwargs)

        except Exception as e:
            # Manejar la excepción y retornar un mensaje personalizado
            return f"No se pudo guardar la entrada. Error: {str(e)}"
    
    def __str__(self):
        return f"{self.tipo} No. {self.number}"
    

class Orderdet(models.Model):   
    order = models.ForeignKey(Order, on_delete=models.CASCADE)     
    item = models.ForeignKey('products.Product', on_delete=models.CASCADE ,verbose_name="Item")
    tipo = models.CharField(editable=False, max_length=20, null=True, blank=True)
    number = models.PositiveIntegerField(editable=False, default=0)
    qty = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False, default= 1, verbose_name=(u'Cantidad'))
    qtyorder = models.DecimalField(editable=False, max_digits=9, decimal_places=2, blank=False, null=False, default= 0)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default= 0.0, verbose_name=(u'Precio'))
    subtotal = models.DecimalField(max_digits=22, decimal_places=2, blank=False, null=False, default= 0.0, verbose_name=(u'SubTotal'))
    comments = models.CharField(max_length=100, blank=True, verbose_name=(u'Comentario'))
    

    def save(self, *args, **kwargs):
        # Establecer tipo y número basándose de la instancia relacionada
        self.tipo, self.number = self.order.tipo, self.order.number

        # Calcular el subtotal al multiplicar el costo por la cantidad
        self.subtotal = self.price * self.qty

        # Establecer qtyrem igual a qty (cantidad)
        self.qtyorder = self.qty
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Detalle"
        verbose_name_plural = "Detalles"

    def __str__(self):
        return f"{self.order} - {self.item}"


