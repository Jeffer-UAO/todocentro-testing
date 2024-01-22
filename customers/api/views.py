from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from customers.api.serializers import DomainSerializer

from .serializers import CustomerSerializer
from customers.models import Customer, Domain


class CustomerApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

class DomainApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()