from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.views import UserApiViewSet, AddressApiViewSet, UserView

router_user = DefaultRouter()

router_user.register(
    prefix='users', basename='users', viewset=UserApiViewSet)

router_user.register(
    prefix='address', basename='address', viewset=AddressApiViewSet)

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/me/', UserView.as_view()),
]
