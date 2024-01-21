from warehome.models import WarehomeDetail, Stock
from carts.models import Cart
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver


@receiver(post_save, sender=WarehomeDetail)
def receiver_product_out(sender, instance, created, **kwargs):      
    if created:        
        try:
            stock = Stock.objects.get(product=instance.product_id, description=instance.description, attribut=instance.attribut)
        except:
            stock = Stock.objects.create(
                product_id=instance.product_id,               
                qty=instance.qty,      
                attribut=instance.attribut,
                description=instance.description
            )
        else:
            stock.qty += instance.qty
            stock.save()
        return stock
    else:
        print("Se crearon cero registros")


@receiver(pre_save, sender=WarehomeDetail)    
def receiver_product_out(sender, instance, **kwargs):
    print("Ooooh... se ejecuto pre_save !!")
    try:
        old = WarehomeDetail.objects.get(
            product=instance.product_id, ProductEntry=instance.ProductEntry, description=instance.description, attribut=instance.attribut)
        if old:
            stock = Stock.objects.get(product_id=instance.product_id, description=instance.description, attribut_id=instance.attribut)
            stock.qty += instance.qty-old.qty            
            stock.save()
            return stock
    except:
        print("El producto no existe en warehomeDetail, Se procedera a crear nuevo registo")


@receiver(pre_delete, sender=WarehomeDetail)
def receiver_product_out(sender, instance, **kwargs):
    try:
        old = WarehomeDetail.objects.get(
            product=instance.product_id, ProductEntry=instance.ProductEntry, attribut=instance.attribut_id, description=instance.description)
        if old:
            stock = Stock.objects.get(product_id=instance.product_id, attribut=instance.attribut_id, description=instance.description)
            stock.qty -= old.qty
            stock.save()
            return stock
    except:
        print("An exception occurred")



# @receiver(pre_save, sender=Cart)
# def product_cart(sender, instance, **kwargs):
#     try:        
#         stock_product = Cart.objects.get_or_create(user=instance.user_id, stock=instance.stock)        
#         if stock_product:           
#             stock_product.quantity += instance.quantity - stock_product.quantity
#             stock_product.save()
#             return stock_product
#     except:
#         print("An exception occurred")
