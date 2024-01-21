from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import OrderSerializer, OrderDetailSerializer
from stores.models import Order, OrderProduct


class OrderApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

# class OrderAPIView(APIView):
#     def post(self, request):
#         order_serializer = OrderSerializer(data=request.data)
#         order_serializer.is_valid(raise_exception=True)

#         order_detail_serializer = OrderDetailSerializer(
#             data=request.data["order_details"], many=True
#         )
#         order_detail_serializer.is_valid(raise_exception=True)

#         with transaction.atomic():
#             order = order_serializer.save()

#             for order_detail_data in request.data["order_details"]:
#                 order_detail = OrderProduct(order=order)
#                 order_detail_serializer = OrderDetailSerializer(
#                     order_detail, data=order_detail_data
#                 )
#                 order_detail_serializer.is_valid(raise_exception=True)
#                 order_detail_serializer.save()

#         return Response(order_serializer.data, status=status.HTTP_201_CREATED)
