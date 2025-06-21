from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from orders.enums import OrderStatus
from orders.models import Order
from payment import robokassa
from .serializers import (
    OrderCreateSerializer,
    OrderRetrieveSerializer,
)


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderRetrieveSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        telegram_id = self.request.query_params.get('telegram_id')
        if telegram_id:
            queryset = queryset.filter(customer__telegram_id=telegram_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = OrderRetrieveSerializer(instance=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    @action(detail=True, methods=['patch'], url_path='cancel')
    def cancel_order(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = OrderStatus.CANCELLED
        order.save()
        serializer = OrderRetrieveSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False,
            methods=['get'],
            permission_classes=[AllowAny],
            url_path='success-payment')
    def success_payment(self, request):
        query_string = request.get_full_path()
        sign = robokassa.result_payment(
            merchant_password_2=settings.MERCHANT_PASSWORD_2,
            request=query_string)
        if 'OK' in sign:
            order_id = request.query_params.get('InvId')
            order = get_object_or_404(Order, pk=order_id)
            order.status = OrderStatus.PAID
            order.save()
            return Response(sign, status=status.HTTP_200_OK)
        return Response(sign, status=status.HTTP_400_BAD_REQUEST)
