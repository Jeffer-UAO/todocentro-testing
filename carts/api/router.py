from rest_framework.routers import DefaultRouter
from carts.api.views import CartApiViewSet

router_cart = DefaultRouter()

router_cart.register(
    prefix='cart', basename='cart', viewset=CartApiViewSet
)
