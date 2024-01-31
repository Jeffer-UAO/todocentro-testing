from django.db.models.signals import post_save
from django.db.models import Sum
from django.db import transaction, IntegrityError
from django.dispatch import receiver
from .models import Ipdet
from inventory.models import Itemact



@receiver(post_save, sender=Ipdet)
def create_or_update_ipdet(sender, instance, created, **kwargs):
    try:      
        with transaction.atomic():                

            # Si es creado, crea un nuevo itemact, de lo contrario, actualiza el existente
            itemact, _ = Itemact.objects.get_or_create(ipdet=instance, defaults={
                'qty': instance.qty,
                'tipo': instance.tipo,
                'number': instance.number,
                'item': instance.item
            })

            if not created:
                # Si no es creado, actualiza el itemact existente
                itemact.qty = instance.qty
                itemact.tipo = instance.tipo
                itemact.number = instance.number
                itemact.item = instance.item
                itemact.save()

            # Actualizar el campo total en el modelo Ip después de guardar un Ipdet
            ip = instance.ip
            ip.total = ip.orderdet_set.filter(tipo='detalle').aggregate(Sum('subtotal'))['subtotal__sum'] or 0.00
            ip.save()

    except IntegrityError as e:
        transaction.set_rollback(True)
        print(f"Error de integridad de base de datos: {e}")

    except Ipdet.DoesNotExist:
        transaction.set_rollback(True)
        print(f"Error: No se encontró un Ipdet para el Ipdet {instance}")

    except Exception as e:
        transaction.set_rollback(True)
        print(f"Error inesperado (Ipdet): {e}")
