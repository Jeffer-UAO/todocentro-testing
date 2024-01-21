from rest_framework.routers import DefaultRouter
from stores.api.views import OrderApiViewSet

router_order = DefaultRouter()
# router_product = DefaultRouter()
# router_product_category = DefaultRouter()
# router_gallery = DefaultRouter()

router_order.register(
    prefix='order', basename='order', viewset=OrderApiViewSet
)
