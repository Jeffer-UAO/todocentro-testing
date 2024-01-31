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
            defaults = {
                'item': instance.item,
                'name_extend': instance.name_extend,
                'images': instance.images,
                'image_alterna': instance.image_alterna,
                'description': instance.description,
                'price1': instance.price1,
                'price2': instance.price2,
                'price_old': instance.price_old,
                'flag': instance.flag,
                'ref': instance.ref,
                'slug': instance.slug,
                'published': instance.published,
                'active': instance.active,
                'soldout': instance.soldout,
                'offer': instance.offer,
                'home': instance.home,
                'created_date': instance.created_date,
                'modified_date': instance.modified_date,
                'domain': tenant_name,
            }

            product_public, created = Product_public.objects.update_or_create(
                codigo=instance.codigo,
                defaults=defaults
            )

            # Actualiza los campos en caso de que haya cambios
            for field, value in defaults.items():
                setattr(product_public, field, value)

            product_public.save()

            if created:
                print("Registro creado con éxito.")
            else:
                print("Registro actualizado con éxito.")
    except Exception as e:
        transaction.set_rollback(True)
        print(f"Error inesperado al sincronizar el producto: {e}")


# Señal para manejar la eliminación de Producto
@receiver(pre_delete, sender=Product)
def delete_product(sender, instance, **kwargs):
    try:
        product_public = Product_public.objects.get(item=instance.item)
        product_public.delete()
    except Product_public.DoesNotExist:
        pass  # No hay nada que eliminar
    except Exception as e:
        transaction.set_rollback(True)
        print(f"Error en la señal pre_delete: {e}")