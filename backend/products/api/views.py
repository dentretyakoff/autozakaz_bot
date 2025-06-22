from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

from products.models import Product
from products.filters import ProductFilter
from .serializers import ProductSerializer, ProductListSerializer


class ProductViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.filter(is_published=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer
