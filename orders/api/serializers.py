from rest_framework.serializers import ModelSerializer
from ..models import Order, Orderdet



class OrderdetSerializer(ModelSerializer):
    class Meta:
        model = Orderdet
        fields = ["comments", "price", "qty", "item"]


class OrderSerializer(ModelSerializer):
    orderdet = OrderdetSerializer(source='orderdet', read_only=True)
    class Meta:
        model = Order
        fields = ["number", "cust", "tipo", "total", "created_date", "concept", "orderdet"]




