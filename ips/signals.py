from django.db import transaction, IntegrityError
from django.db.models import F
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import Ipdet, Itemact, ItemactItem


@receiver(post_save, sender=Ipdet)
def create_or_update_itemact(sender, instance, created, **kwargs):
    try:     

        with transaction.atomic():
            if created:
                # Si es un nuevo Ipdet, crea un nuevo Itemact
                itemact = Itemact.objects.create(
                    ipdet=instance,
                    qty=instance.qty,
                    tipo=instance.tipo,
                    number=instance.number,
                    item=instance.item
                )
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

    except IntegrityError as e:      
        transaction.set_rollback(True)
        print(f"Error de integridad de base de datos: {e}")

    except Itemact.DoesNotExist:           
        transaction.set_rollback(True)
        print(f"Error: No se encontró un Itemact para el Ipdet {instance}")

    except Exception as e:       
        transaction.set_rollback(True)
        print(f"Error inesperado (Itemact): {e}")



@receiver(post_save, sender=Itemact)
def actualizar_cantidades(sender, instance, **kwargs):
    
    try:
        with transaction.atomic():
            # Obtener el código del producto relacionado con el movimiento
            codigo_producto = instance.item.codigo

            # Calcular la cantidad actual utilizando agregación
            cantidad_actual = Itemact.objects.filter(item__codigo=codigo_producto).aggregate(
                cantidad_actual=Sum('qty')
            )['cantidad_actual']

            # Obtener el datos del producto
            nombre_producto = instance.item.name_extend
            item_uuid = instance.item.item            
            images = getattr(instance.item.images, 'images', "")
            image_alterna = getattr(getattr(instance.item, 'image_alterna', ""), 'campo_deseado', "")
            # description = getattr(instance.item, 'description', None)
            # price1 = getattr(instance.item, 'price1', None)
            # price2 = getattr(instance.item, 'price2', None)
            # price_old = getattr(instance.item, 'price_old', None)
            # flag = getattr(instance.item, 'flag', None)
            # ref = getattr(instance.item, 'ref', None)        
            # slug = getattr(instance.item, 'slug', None)
            # active = getattr(instance.item, 'active', None)
            # soldout = getattr(instance.item, 'soldout', None)
            # offer = getattr(instance.item, 'offer', None)
            # home =getattr(instance.item, 'home', None)
           
           

            # Actualizar o crear la instancia en ItemactItem
            itemact_item, created = ItemactItem.objects.update_or_create(
                item=instance.item,
                defaults={'cantidad_actual': cantidad_actual, 'nombre': nombre_producto, 'item': instance.item, 
                           'uuid': item_uuid, 'images': images, 'image_alterna': image_alterna
                        #     , 'description': description,
                        #   'price1': price1, 'price2': price2, 'price_old': price_old, 'flag': flag, 'ref': ref,
                        #   'slug': slug, 'active': active, 'soldout': soldout, 'offer': offer, 'home': home
                          } 
            )
            # Puedes imprimir un mensaje si se crea una nueva instancia
            if created:
                print(f"ItemactItem creado con éxito para {nombre_producto}")
            else:
                # Si no es nuevo, actualizar la instancia existente
                itemact_item.cantidad_actual = cantidad_actual
                itemact_item.save()
                # Imprimir otro mensaje si se actualiza correctamente
                print(f"Cantidad actualizada de {nombre_producto} a {cantidad_actual} por el movimiento #{instance.pk}")    

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