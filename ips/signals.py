from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import Ipdet, Itemact



@receiver(post_save, sender=Ipdet)
def create_or_update_itemact(sender, instance, created, **kwargs):
    try:
        with transaction.atomic():
            if created:
                # Si es un nuevo Ipdet, crea un nuevo Itemact
                itemact = Itemact.objects.create(ipdet=instance, qty=instance.qty, tipo=instance.tipo, number=instance.number, item= instance.item)
            else:
                # Si se está actualizando un Ipdet, actualiza el Itemact correspondiente
                itemact = Itemact.objects.select_for_update().get(ipdet=instance)
                itemact.qty = instance.qty
                itemact.tipo = instance.tipo
                itemact.number = instance.number   
                itemact.item = instance.item           
                itemact.save()
            
            # Actualizar el campo total en el modelo Ip después de guardar un Ipdet
            ip = instance.ip
            ip.total = ip.ipdet_set.aggregate(Sum('subtotal'))['subtotal__sum'] or 0.00
            ip.save()

    except Itemact.DoesNotExist:
        # Manejar la excepción si el Itemact no existe
        print(f"Error: No se encontró un Itemact para el Ipdet {instance}")
    except Exception as e:
        # Manejar otras excepciones
        print(f"Error inesperado: {e}")


