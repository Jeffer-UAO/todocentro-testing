from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Product
from customers.models import Product_public
from django.db import transaction




@receiver(post_save, sender=Product)
def sync_producto(sender, instance, created, **kwargs):
    print("Signal activada.")
    
    if created:
        try:
            with transaction.atomic():
                product_public = Product_public.objects.get(codigo=instance.codigo)
                # Actualizar los campos
                product_public.name_extend = instance.name_extend
                product_public.images = instance.images
                # ... (actualizar otros campos)
                product_public.save()
        except Product_public.DoesNotExist:
            # Si no se encuentra, crear un nuevo objeto
            product_public = Product_public.objects.create(
                codigo=instance.codigo,
                name_extend=instance.name_extend,
                images=instance.images,
                # ... (otros campos)
            )
            print("Registro creado con éxito.")
        except Exception as e:
            print(f"Error inesperado: {e}")
    else:
        print("No se crearon registros porque la instancia ya existía.")

        

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