from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Product
from customers.models import Product_public



@receiver(post_save, sender=Product)
def sync_producto(sender, instance, created, **kwargs):
    print("Signal activada.")
    if created:
        try:
            product_public = Product_public.objects.get(codigo=instance.codigo)
            product_public.codigo = instance.codigo
            product_public.name_extend = instance.name_extend
            product_public.images = instance.images
            product_public.image_alterna = instance.image_alterna
            product_public.description = instance.description
            product_public.price1 = instance.price1
            product_public.price2 = instance.price2
            product_public.price_old = instance.price_old
            product_public.flag = instance.flag
            product_public.ref = instance.ref 
            product_public.slug = instance.slug 
            product_public.active = instance.active       
            product_public.soldout = instance.soldout 
            product_public.offer = instance.offer 
            product_public.home = instance.home
            product_public.created_date = instance.created_date 
            product_public.modified_date = instance.modified_date 
            product_public.save()
        except:
            product = Product_public.objects.create(
                codigo = instance.codigo,
                name_extend = instance.name_extend,
                images = instance.images,
                image_alterna = instance.image_alterna,
                description = instance.description,
                price1 = instance.price1,
                price2 = instance.price2,
                price_old = instance.price_old,
                flag = instance.flag,
                ref = instance.ref ,
                slug = instance.slug, 
                active = instance.active,       
                soldout = instance.soldout, 
                offer = instance.offer, 
                home = instance.home,
                created_date = instance.created_date ,
                modified_date = instance.modified_date,
            )
            product.save()
            return product       
    else:
        print("Se crearon cero registros")

# # Señal para manejar la eliminación de Producto
# @receiver(pre_delete, sender=Producto)
# def delete_copia_producto(sender, instance, **kwargs):
#     try:
#         copia_producto = CopiaProducto.objects.get(pk=instance.pk)
#         copia_producto.delete()
#     except CopiaProducto.DoesNotExist:
#         pass  # No hay nada que eliminar
#     except Exception as e:
#         print(f"Error en la señal pre_delete: {e}")