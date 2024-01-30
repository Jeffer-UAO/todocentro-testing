from django.db.models import F
from django.db.models.signals import post_save, pre_delete
from django.db.models import Sum
from django.db import transaction, IntegrityError
from django.dispatch import receiver
from inventory.models import Itemact, ItemactItem



@receiver(post_save, sender=Itemact)
def actualizar_cantidades(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            # Obtener el producto relacionado con el movimiento
            item = instance.item

            # Calcular la cantidad actual utilizando agregación
            cantidad_actual = Itemact.objects.filter(item__codigo=item.codigo).aggregate(
                cantidad_actual=Sum('qty')
            )['cantidad_actual']

            # Actualizar o crear la instancia en ItemactItem
            itemact_item, created = ItemactItem.objects.update_or_create(
                item=item,
                defaults={
                    'cantidad_actual': cantidad_actual,
                    'nombre': item.name_extend,
                    'item': item,
                    'uuid': item.item,
                    'slug': item.slug,
                    'price1': item.price1 or 0,
                    'price2': item.price2 or 0,
                    'price_old': item.price_old or 0,
                    'images': item.images or "",
                    'image_alterna': item.image_alterna or "",
                    'description': item.description or "",
                    'flag': item.flag or "",
                    'ref': item.ref or "",
                    'active': item.active or "True",
                    'soldout': item.soldout or "False",
                    'offer': item.offer or "False",
                    'home': item.home or "False"
                }
            )

            # Puedes imprimir un mensaje si se crea una nueva instancia
            if created:
                print(f"ItemactItem creado con éxito para {item.name_extend}")
            else:
                # Si no es nuevo, actualizar la instancia existente
                itemact_item.cantidad_actual = cantidad_actual
                itemact_item.save()
                # Imprimir otro mensaje si se actualiza correctamente
                print(f"Cantidad actualizada de {item.name_extend} a {cantidad_actual} por el movimiento #{instance.pk}")

    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante la operación
        transaction.set_rollback(True)
        print(f"Error inesperado - (ItemactItem): {e}")



@receiver(pre_delete, sender=Itemact)
def restar_cantidades(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            # Obtener el código del producto relacionado con el movimiento
            codigo_producto = instance.item.codigo

            # Restar la cantidad actual en ItemactItem
            ItemactItem.objects.filter(item__codigo=codigo_producto).update(
                cantidad_actual=F('cantidad_actual') - instance.qty
            )

            print(f"Cantidad actualizada después de eliminar el movimiento #{instance.pk}")

    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante la operación
        transaction.set_rollback(True)
        print(f"Error inesperado: {e}")