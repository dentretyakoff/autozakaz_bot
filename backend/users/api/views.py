from rest_framework import mixins, viewsets

from users.models import CustomerBot
from .serializers import (
    CustomerBotCreateSerializer,
    CustomerBotUpdateSerializer,
    CustomerBotRetrieveSerializer,
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
