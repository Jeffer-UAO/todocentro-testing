from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Order, Orderdet
from .serializers import OrderdetSerializer, OrderSerializer


class OrderApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['slug']

class OrderdetApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderdetSerializer
    queryset = Orderdet.objects.all()
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['slug']
