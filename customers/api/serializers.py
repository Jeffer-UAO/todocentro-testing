from rest_framework.serializers import ModelSerializer
from customers.models import Customer

# from warehome.api.serializers import StockSerializer

class CustomerSerializer(ModelSerializer):
    # stock_data = StockSerializer(source='stock', read_only=True)

    class Meta:
        model = Customer
        fields = ['id_n', 'company' ]

