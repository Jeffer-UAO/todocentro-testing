from django.db import transaction, IntegrityError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import Oedet
from inventory.models import Itemact


@receiver(post_save, sender=Oedet)
def create_or_update_itemact(sender, instance, created, **kwargs):
    try:      
        with transaction.atomic():
            # Calcula la cantidad para el nuevo Itemact
            qty = instance.qty * -1

            # Si es creado, crea un nuevo Itemact, de lo contrario, actualiza el existente
            itemact, _ = Itemact.objects.get_or_create(oedet=instance, defaults={
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
            oe = instance.oe         
            oe.total = oe.oedet_set.aggregate(Sum('subtotal'))['subtotal__sum'] or 0.00
            oe.save()
         

    except IntegrityError as e:
        transaction.set_rollback(True)
        print(f"Error de integridad de base de datos: {e}")

    except Itemact.DoesNotExist:
        transaction.set_rollback(True)
        print(f"Error: No se encontró un Itemact para el Ipdet {instance}")

    except Exception as e:
        transaction.set_rollback(True)
        print(f"Error inesperado (Itemact): {e}")



@receiver(post_delete, sender=Oedet)
def restar_total(sender, instance, **kwargs):
    try:
        with transaction.atomic():
           
            oe = instance.oe          
            oe.total = oe.oedet_set.aggregate(Sum('subtotal'))['subtotal__sum'] or 0.00
            oe.save()
            print(f"Se elminaron productos")
            
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante la operación
        transaction.set_rollback(True)
        print(f"Error inesperado: {e}")