from rest_framework.serializers import ModelSerializer
from ..models import Order, Orderdet


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ["concept"]


class OrderdetSerializer(ModelSerializer):
    class Meta:
        model = Orderdet
        fields = ["concept", "price", "qty", "item"]
    