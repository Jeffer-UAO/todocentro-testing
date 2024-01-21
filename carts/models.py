from django.db import models
from accounts.models import Account
from warehome.models import Stock

# Create your models here.
class Cart(models.Model):
    quantity = models.IntegerField()
    nota = models.CharField(max_length=50, null=True, blank=True, verbose_name=(u'Descripción'))
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=(u'Creado'))
    modified_date = models.DateTimeField(
        auto_now=True, verbose_name=(u'Modificado'))
    pending = models.BooleanField(default=True, verbose_name=(u'Pendiente'))    
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, verbose_name=(u'Stock'))
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name=(u'Usuario'))
    

    # def save(self, *args, **kwargs):

    #         created = Cart.objects.filter(user=self.user_id)
    #         if not created:               
    #             created = Cart.objects.create(
    #             quantity=self.quantity,               
    #             pending=self.pending,      
    #             stock_id=self.stock_id,
    #             user_id=self.user_id
    #         )
    #         else:
    #             created.quantity = self.quantity
    #             created.save()

    #             super(Cart, self).save(*args, **kwargs)
    


    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    def __str__(self):
        return str(self.stock)


    