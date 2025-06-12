from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    manufacturer = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Product
        fields = (
            'id',
            'manufacturer',
            'code',
            'name',
            'description',
            'price',
            'period_min',
            'is_actual',
            'is_published',
            'csv_price',
            'product_code'
        )
