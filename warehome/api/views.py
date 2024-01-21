from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from .serializers import ProductOutSerializer, StockSerializer, WarehomeDetailSerializer
# from customers.
from warehome.models import ProductOut, Stock, WarehomeDetail


class ProductOutApiViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = ProductOutSerializer
    queryset = ProductOut.objects.all()


class WarehomeDetailApiViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = WarehomeDetailSerializer
    queryset = WarehomeDetail.objects.all()


class StockApiViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = StockSerializer
    queryset = Stock.objects.all().order_by('product_id')
    # filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    # search_fields = ['product_id']
    # filterset_fields = {'qty':['gte']}
