from rest_framework.routers import DefaultRouter
from .views import OrderApiViewSet, OrderdetApiViewSet

router_ordere = DefaultRouter()
router_orderdet = DefaultRouter()


router_ordere.register(
    prefix='ordere', basename='ordere', viewset=OrderApiViewSet 
)

router_orderdet.register(
    prefix='orderdet', basename='orderdet', viewset=OrderdetApiViewSet   
)