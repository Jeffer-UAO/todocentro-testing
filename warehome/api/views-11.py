from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
#from django.db import transaction
from rest_framework import filters


from warehome.models import WarehomeDetail, ProductOut, ProductEntry, Stock
from .serializers import ProductOutSerializer, StockSerializer


class ProductOutApiViewSet(ModelViewSet):
    queryset = ProductOut.objects.all()
    queryset = ProductEntry.objects.all()
    serializer_class = ProductOutSerializer

    def create(self, request):
        serializer = ProductOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_out = serializer.save()

        # crear la transacción entre entradas y salidas
        products_entry = request.data.get('products_entry')
        products_out = request.data.get('products_out')

        for product in products_entry:
            # obtener los detalles de inventario del producto
            product_entry_detail = WarehomeDetail.objects.filter(
                product=product['product'])

            # actualizar la cantidad de un producto en inventario
            for product_entry in product_entry_detail:
                product_entry.qty -= product['qty']
                product_entry.save()

            # crear detalle de salida
            WarehomeDetail.objects


class StockApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = StockSerializer
    queryset = Stock.objects.all().order_by('product_id')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['product_id']
    filterset_fields = {'qty':['gte']}

