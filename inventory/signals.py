from django.db.models import F, Value, Case, When, IntegerField
from django.db.models.signals import post_save, pre_delete
from django.db.models import Sum
from django.db import transaction
from django.dispatch import receiver
from inventory.models import Itemact, ItemactItem
from django.db.models.functions import Coalesce



@receiver(post_save, sender=Itemact)
def actualizar_cantidades(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            # Obtener el producto relacionado con el movimiento
            item = instance.item
     
            # Calcular la cantidad actual en Pedidos (Reserva)
            qtyorder_total = Itemact.objects.filter(item__codigo=item.codigo).aggregate(
                qtyorder_total=Sum('qtyorder')
            )['qtyorder_total']
          

            # Calcular la cantidad actual utilizando agregación (Stock)
            cantidad_actual = Itemact.objects.filter(item__codigo=item.codigo).aggregate(
                cantidad_actual=Sum('qty')
            )['cantidad_actual']



            # Disponibilidad del producto (stock - reserva)
            available = cantidad_actual
            # available = cantidad_actual - qtyorder_total

            # Actualizar o crear la instancia en ItemactItem
            itemact_item, created = ItemactItem.objects.update_or_create(
                item=item,             
                defaults={
                    'cantidad_actual': cantidad_actual,
                    'qtyorder' : qtyorder_total,
                    'available' : available,
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

            # Controla las cantidades en itemactitem cuando se elimina un registro
            # (cantidad_actual, available, qtyorder)

            if instance.qtyorder == 0:
                ItemactItem.objects.filter(item__codigo=codigo_producto).update(
                    cantidad_actual = F('cantidad_actual') - instance.qty,                   
                    available = F('available') - instance.qty                
                )
            
            if instance.qtyorder > 0:
                print(f'qtyorder = {instance.qtyorder}')
                ItemactItem.objects.filter(item__codigo=codigo_producto).update(
                    cantidad_actual = F('cantidad_actual') - instance.qty,
                    qtyorder=F('qtyorder') + instance.qty,
                    available = F('available') - instance.qty                
                )
                                 
                

                # raise ValueError("No se puede eliminar este elemento porque hay pedidos pendientes 
                #                  de este artículo.") 
            # if instance.qty > 0:
            #     ItemactItem.objects.filter(item__codigo=codigo_producto).update(
            #         cantidad_actual = F('cantidad_actual') - instance.qty,
            #         available = F('available') - instance.qty                
            #     )
            # if instance.qty < 0:
            #     ItemactItem.objects.filter(item__codigo=codigo_producto).update(
            #         cantidad_actual = F('cantidad_actual') - instance.qty,
            #         available = F('available') - instance.qty                
            #     )
            # if instance.qty == 0:
            #     ItemactItem.objects.filter(item__codigo=codigo_producto).update(
            #         cantidad_actual = F('cantidad_actual') - instance.qty,
            #         qtyorder=Coalesce(F('qtyorder') - instance.qtyorder, Value(0)),
            #         available = F('available') + instance.qtyorder                
            #     )

            print(f"Cantidad actualizada después de eliminar el movimiento #{instance.pk}")
            # order_total = F('qtyorder') + F('qtypurchase')  # Sum

    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante la operación
        transaction.set_rollback(True)
        print(f"Error inesperado: {e}")