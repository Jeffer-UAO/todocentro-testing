from django.db.models.signals import post_save
from django.db.models import Sum
from django.db import transaction, IntegrityError
from django.dispatch import receiver
from .models import Ipdet



@receiver(post_save, sender=Ipdet)
def create_or_update_ipdet(sender, instance, created, **kwargs):
    try:      
        with transaction.atomic():                

            # Si es creado, crea un nuevo ipdet, de lo contrario, actualiza el existente
            ipdet, _ = Ipdet.objects.get_or_create(ipdet=instance, defaults={
                'qty': instance.qty,
                'tipo': instance.tipo,
                'number': instance.number,
                'item': instance.item
            })

            if not created:
                # Si no es creado, actualiza el ipdet existente
                ipdet.qty = instance.qty
                ipdet.tipo = instance.tipo
                ipdet.number = instance.number
                ipdet.item = instance.item
                ipdet.save()

            # Actualizar el campo total en el modelo Ip después de guardar un Ipdet
            ip = instance.ip
            ip.total = ip.ipdet_set.aggregate(Sum('subtotal'))['subtotal__sum'] or 0.00
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
