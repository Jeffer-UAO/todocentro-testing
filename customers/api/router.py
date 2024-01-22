from rest_framework.routers import DefaultRouter
from customers.api.views import DomainApiViewSet

route_domain = DefaultRouter()

route_domain.register(
    prefix='domain', basename='domain', viewset=DomainApiViewSet 
)