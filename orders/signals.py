from django.db import transaction, IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import Orderdet 
from inventory.models import Itemact


@receiver(post_save, sender=Orderdet)
def create_or_update_itemact(sender, instance, created, **kwargs):
    try:      
        with transaction.atomic():
            # Calcula la cantidad para el nuevo Itemact
            qty = instance.qty * -1

            # Si es creado, crea un nuevo Itemact, de lo contrario, actualiza el existente
            itemact, _ = Itemact.objects.get_or_create(orderdet=instance, defaults={
                'qty': qty,
                'tipo': instance.tipo,
                'number': instance.number,
                'item': instance.item
            })

            if not created:
                # Si no es creado, actualiza el Itemact existente
                itemact.qty = qty
                itemact.tipo = instance.tipo
                itemact.number = instance.number
                itemact.item = instance.item
                itemact.save()

            # Actualiza el campo total en el modelo Order después de guardar un Orderdet
            order = instance.order
            order_total_before = order.total  # Guarda el valor antes de la actualización
            order.total = order.orderdet_set.aggregate(Sum('subtotal'))['subtotal__sum'] or 0.00
            order.save()
            print(f"Order #{order.pk} - Total antes: {order_total_before}, Total después: {order.total}")


    except IntegrityError as e:
        transaction.set_rollback(True)
        print(f"Error de integridad de base de datos: {e}")

    except Itemact.DoesNotExist:
        transaction.set_rollback(True)
        print(f"Error: No se encontró un Itemact para el Ipdet {instance}")

    except Exception as e:
        transaction.set_rollback(True)
        print(f"Error inesperado (Itemact): {e}")
