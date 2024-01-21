from rest_framework.serializers import ModelSerializer
from carts.models import Cart


from warehome.api.serializers import StockSerializer


class CartSerializer(ModelSerializer):
    stock_data = StockSerializer(source='stock', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'quantity', 'nota', 'pending', 'stock', 'stock_data', 'user', 'modified_date', 'created_date']
