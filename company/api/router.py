from rest_framework.routers import DefaultRouter
from company.api.views import CompanyApiViewSet

router_company = DefaultRouter()

router_company.register(
    prefix='company', basename='company', viewset=CompanyApiViewSet
)
