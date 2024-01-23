from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Product
from customers.models import Product_public
from django.db import transaction


@receiver(post_save, sender=Product)
def sync_producto(sender, instance, **kwargs):  
    try:
        with transaction.atomic():
            product_public, _ = Product_public.objects.get_or_create(codigo=instance.codigo)

            # Actualizar los campos en cualquier caso (creación o actualización)
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
            if not kwargs['created']:  # Si se está editando el product
                print('Se ha EDITADO un producto')
            else:                       # Si se está creando uno nuevo
                print('Se ha CREATDO un producto')
    except Exception as e:
        print("Error al sincronizar el producto")
        raise e
        
    
        # print(f"Error inesperado: {e}")



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