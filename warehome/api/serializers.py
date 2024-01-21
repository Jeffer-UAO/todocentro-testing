from rest_framework.serializers import ModelSerializer
from warehome.models import ProductOut, Stock, DocumentOut, WarehomeDetail
from products.api.serializers import ProductSerializer, CategoryProductSerializer
from customers.api.serializers import CustomerSerializer
# from warehome.api.serializers import Out

class DocumentOutSerializer(ModelSerializer):
    class Meta:
        model = DocumentOut
        fields = ['type', 'description']


class ProductOutSerializer(ModelSerializer):
    customer_data = CustomerSerializer(source='customer', read_only=True)
    document_data = DocumentOutSerializer(source='type', read_only= True)

    class Meta:
        model = ProductOut
        fields = ['document_data', 'number', 'customer_data', 'created_date', 'deudate', 'created_date_sistem', 'comments' ]


class WarehomeDetailSerializer(ModelSerializer):
    # product = ProductSerializer()
    class Meta:
        model = WarehomeDetail
        fields = ['id', 'product', 'attribut', 'description', 'qty', 'costo', 'iva', 'ProductEntry', 'ProductOut']



class StockSerializer(ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Stock
        fields = ['id', 'qty', 'product', 'description', 'attribut']
