from rest_framework import serializers

from products.models import Product


class ProductListSerializer(serializers.ModelSerializer):
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
            'is_published',
            'product_code',
        )


class ProductSerializer(ProductListSerializer):
    quantity = serializers.SerializerMethodField()
    cartitem_id = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

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
            'is_published',
            'product_code',
            'cartitem_id',
            'quantity',
            'min_qty',
            'qty',
            'total_price'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        self.customer = None
        self.telegram_id = request.query_params.get('telegram_id')
        if self.telegram_id:
            from users.models import CustomerBot
            try:
                self.customer = (
                    CustomerBot.objects.select_related('cart')
                    .prefetch_related('cart__items')
                    .get(telegram_id=self.telegram_id))
            except CustomerBot.DoesNotExist:
                self.customer = None

    def get_quantity(self, obj):
        if self.customer:
            cartitem = self.customer.cart.items.filter(product=obj).first()
            return getattr(cartitem, 'quantity', 0)
        return None

    def get_total_price(self, obj):
        if self.customer:
            return self.customer.cart.total_price
        return None

    def get_cartitem_id(self, obj):
        if self.customer:
            cartitem = self.customer.cart.items.filter(product=obj).first()
            return getattr(cartitem, 'id', None)
        return None
