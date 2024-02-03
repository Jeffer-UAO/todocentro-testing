from rest_framework.serializers import ModelSerializer
from ..models import Order, Orderdet
from rest_framework import serializers



class OrderdetSerializer(ModelSerializer):
    class Meta:
        model = Orderdet
        fields = ["comments", "price", "qty"]


class OrderSerializer(serializers.ModelSerializer):
    orderdetData = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["number", "cust", "tipo", "total", "created_date", "concept", "orderdetData"]

    def get_orderdetData(self, obj):
        orderdet_instances = obj.orderdet_set.all()  # Asegúrate de que el nombre sea correcto según tu modelo de datos
        orderdet_serializer = OrderdetSerializer(orderdet_instances, many=True)
        return orderdet_serializer.data


