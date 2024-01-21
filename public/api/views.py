from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from public.api.serializers import DomainSerializer
from customers.models import Domain

class DomainApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()