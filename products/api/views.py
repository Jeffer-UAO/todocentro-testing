from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework import filters


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from customers.models import CustomerDomain
# from django_tenants.utils import schema_context


from products.models import Gallery, Category, Product, CategoryProduct, Attribut
from products.api.serializers import GallerySerializer, CategorySerializer, ProductSerializer, CategoryProductSerializer, AttributSerializer


class CategoryApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-created_date')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']


class ProductApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-created_date')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['flag', 'name_extend', 'description', 'ref', 'codigo', 'price1']
    filterset_fields = ['slug', 'flag', 'active']


class ProductOEApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(offer=True) | Q(home=True)).order_by('name_extend')
        return queryset


class CategoryProductApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategoryProductSerializer
    queryset = CategoryProduct.objects.all().order_by('-created_date')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


class GalleryApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']


class AttributApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AttributSerializer
    queryset = Attribut.objects.all().order_by('id') 
    

# class CustomerDomainAPIView(APIView):
#     def get(self, request, format=None):
       
#         domains = CustomerDomain.objects.all()

#         # Puedes personalizar la serialización según tus modelos y necesidades
#         serialized_domains = [{'id': domain.id, 'name': domain.name} for domain in domains]

#         return Response(serialized_domains, status=status.HTTP_200_OK)
