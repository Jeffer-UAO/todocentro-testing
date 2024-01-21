from rest_framework.routers import DefaultRouter
from warehome.api.views import ProductOutApiViewSet, StockApiViewSet, WarehomeDetailApiViewSet


router_out = DefaultRouter()
router_stock = DefaultRouter()
router_warehomedetail = DefaultRouter()

router_out.register(
    prefix='out', basename='out', viewset=ProductOutApiViewSet
)

router_warehomedetail.register(
    prefix='warehomedetail', basename='warehomedetail', viewset=WarehomeDetailApiViewSet
)

router_stock.register(
    prefix='stock', basename='stock', viewset=StockApiViewSet

)
