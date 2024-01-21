from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from company.models import Company
from company.api.serializers import CompanySerializer



class CompanyApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    
