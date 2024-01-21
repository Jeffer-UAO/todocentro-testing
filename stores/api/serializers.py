from rest_framework.serializers import ModelSerializer
from stores.models import Order, OrderProduct


# from warehome.api.serializers import StockSerializer


class OrderSerializer(ModelSerializer):
    # stock_data = StockSerializer(source='stock', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'payment', 'order_note', 'total', 'sub_total', 'discount', 'address', 'tax', 'status', 'ip', 'created_at', 'updated_at']


class OrderDetailSerializer(ModelSerializer):
    # stock_data = StockSerializer(source='stock', read_only=True)
    class Meta:
        model = OrderProduct
        fields = ['id', 'user', 'payment', 'order', 'product', 'quantity', 'product_price', 'ordered', 'created_at', 'updated_at']
