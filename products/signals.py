from django.db.models.signals import post_save, pre_delete
from django_tenants.utils import connection
from django.dispatch import receiver
from .models import Product
from customers.models import Product_public
from django.db import transaction


@receiver(post_save, sender=Product)
def sync_producto(sender, instance, **kwargs):  
    try:              
        tenant_name = connection.tenant.schema_name
        with transaction.atomic():
            product_public, created = Product_public.objects.get_or_create(codigo=instance.codigo,
                defaults={
                'item' : instance.itemId,
                'name_extend' : instance.name_extend,
                'images' : instance.images,
                'image_alterna' :  instance.image_alterna,
                'description' :  instance.description,
                'price1' :  instance.price1,
                'price2' :  instance.price2,
                'price_old' :  instance.price_old,
                'flag' :  instance.flag,
                'ref' :  instance.ref,
                'slug' :  instance.slug,
                'active' :  instance.active,
                'soldout' :  instance.soldout,
                'offer' :  instance.offer,
                'home' :  instance.home,
                'created_date' :  instance.created_date,
                'modified_date' :  instance.modified_date,
                'domain' : tenant_name,             
                }
            )
            product_public.name_extend = instance.itemId
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
            product_public.domain = tenant_name                    
            product_public.save()
            if created:
                print("Registro creado con éxito.")
            else:
                print("Registro actualizado con éxito.")
    except Exception as e:
        print(f"Error inesperado al sincronizar el producto: {e}")


# # Señal para manejar la eliminación de Producto
# @receiver(pre_delete, sender=Product)
# def delete_product(sender, instance, **kwargs):
#     try:
#         product_public = Product_public.objects.get(id=instance.id)
#         product_public.delete()
#     except Product_public.DoesNotExist:
#         pass  # No hay nada que eliminar
#     except Exception as e:
#         print(f"Error en la señal pre_delete: {e}")