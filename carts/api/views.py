from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


from carts.models import Cart
from carts.api.serializers import CartSerializer



class CartApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pending', 'user']
