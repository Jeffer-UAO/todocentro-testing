from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Ip, Ipdet, Itemact



@receiver(post_save, sender=Ipdet)
def create_or_update_itemact(sender, instance, created, **kwargs):
    try:
        with transaction.atomic():
            if created:
                # Si es un nuevo Ipdet, crea un nuevo Itemact
                itemact = Itemact.objects.create(ipdet=instance, qty=instance.qty, tipo=instance.tipo, number=instance.number)
            else:
                # Si se está actualizando un Ipdet, actualiza el Itemact correspondiente
                itemact = Itemact.objects.select_for_update().get(ipdet=instance)
                itemact.qty = instance.qty
                itemact.tipo = instance.tipo
                itemact.number = instance.number
                itemact.save()
    except Itemact.DoesNotExist:
        # Manejar la excepción si el Itemact no existe
        print(f"Error: No se encontró un Itemact para el Ipdet {instance}")
    except Exception as e:
        # Manejar otras excepciones
        print(f"Error inesperado: {e}")


@receiver(pre_save, sender=Ip)
def set_tipo_on_creation(sender, instance, **kwargs):
    # Si el objeto Ip está siendo creado (no existe en la base de datos)
    if not instance.pk:
        # Permitir la edición del campo tipo solo durante la creación
        instance._meta.get_field('tipo').editable = True
    else:
        # Si el objeto ya existe, no permitir la edición del campo tipo
        instance._meta.get_field('tipo').editable = False