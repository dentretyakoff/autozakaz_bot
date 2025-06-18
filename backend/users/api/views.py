from rest_framework import mixins, viewsets

from users.models import CustomerBot, Cart, CartItem
from .serializers import (
    CustomerBotCreateSerializer,
    CustomerBotUpdateSerializer,
    CustomerBotRetrieveSerializer,
    CartSerializer,
    CartItemSerializer
)


class CustomerBotViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = CustomerBot.objects.all()
    lookup_field = 'telegram_id'
    serializer_class = CustomerBotRetrieveSerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return CustomerBotUpdateSerializer
        if self.action == 'create':
            return CustomerBotCreateSerializer
        return CustomerBotRetrieveSerializer


class CartViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'customer__telegram_id'

    def get_queryset(self):
        return (super().get_queryset()
                .select_related('customer')
                .prefetch_related('items'))


class CartItemViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        telegram_id = self.request.query_params.get('telegram_id')
        queryset = CartItem.objects.all().select_related(
            'product', 'product__manufacturer')
        if telegram_id:
            queryset = queryset.filter(
                cart__customer__telegram_id=telegram_id)
        return queryset
