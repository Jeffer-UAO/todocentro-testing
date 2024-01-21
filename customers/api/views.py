from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .serializers import CustomerSerializer
from customers.models import Customer


class CustomerApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()