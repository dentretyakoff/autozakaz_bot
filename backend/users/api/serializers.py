from rest_framework import serializers

from users.models import CustomerBot, Cart, CartItem


class CustomerBotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerBot
        fields = ('telegram_id', 'nickname', 'gdpr_accepted')


class CustomerBotUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerBot
        fields = ('telegram_id', 'nickname', 'gdpr_accepted', 'phone')
        read_only_fields = ('telegram_id',)


class CustomerBotRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerBot
        fields = ('id', 'telegram_id', 'nickname', 'gdpr_accepted', 'phone')


class CartItemSerializer(serializers.ModelSerializer):
    telegram_id = serializers.CharField(write_only=True, required=False)
    product_name = serializers.CharField(
        source='product.name', read_only=True
    )
    code = serializers.CharField(
        source='product.code', read_only=True
    )
    product_code = serializers.CharField(
        source='product.product_code', read_only=True
    )
    price = serializers.IntegerField(
        source='product.price', read_only=True
    )
    manufacturer = serializers.CharField(
        source='product.manufacturer.name', read_only=True
    )

    class Meta:
        model = CartItem
        fields = (
            'id',
            'telegram_id',
            'cart',
            'product',
            'product_name',
            'code',
            'product_code',
            'manufacturer',
            'quantity',
            'price',
        )
        read_only_fields = ('id', 'cart', 'product_name', 'price')

    def validate(self, data):
        if self.instance is None:
            telegram_id = data.pop('telegram_id', None)
            if not telegram_id:
                raise serializers.ValidationError(
                    {'telegram_id': 'Обязательное поле.'})
            try:
                customer = CustomerBot.objects.get(telegram_id=telegram_id)
            except CustomerBot.DoesNotExist:
                raise serializers.ValidationError(
                    {'telegram_id': 'Пользователь с таким Telegram ID не найден.'})  # noqa
            if not hasattr(customer, 'cart'):
                raise serializers.ValidationError(
                    {'telegram_id': 'У пользователя нет корзины.'})
            data['cart'] = customer.cart
        return data


class CartSerializer(serializers.ModelSerializer):
    telegram_id = serializers.CharField(write_only=True, required=False)
    customer = CustomerBotRetrieveSerializer(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = (
            'id',
            'telegram_id',
            'customer',
            'payment_method',
            'payment_method_display',
            'comment',
            'total_price',
            'items',
        )
        read_only_fields = ('id', 'customer', 'total_price', 'items')

    def validate(self, data):
        if self.instance is None:
            telegram_id = data.pop('telegram_id', None)
            if not telegram_id:
                raise serializers.ValidationError(
                    {'telegram_id': 'Обязательное поле.'})
            try:
                customer = CustomerBot.objects.get(telegram_id=telegram_id)
            except CustomerBot.DoesNotExist:
                raise serializers.ValidationError(
                    {'telegram_id': 'Пользователь с таким Telegram ID не найден.'})  # noqa
            data['customer'] = customer
        return data

    def create(self, validated_data):
        cart, _ = Cart.objects.get_or_create(
            customer=validated_data.get('customer')
        )
        return cart
