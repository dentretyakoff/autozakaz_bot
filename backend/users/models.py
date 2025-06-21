from django.db import models
from django.core.validators import RegexValidator

from base.models import BaseModel
from base.enums import PaymentMethod
from products.models import Product


class CustomerBot(BaseModel):
    telegram_id = models.PositiveBigIntegerField(
        'Телеграм ID',
        unique=True
    )
    nickname = models.CharField(
        'Никнейм',
        null=True,
        blank=True,
        max_length=255
    )
    gdpr_accepted = models.BooleanField(
        default=False,
        verbose_name='Согласие на ПД',
        help_text='Статус согласия на обработку перс. данных'
    )
    phone = models.CharField(
        validators=[
            RegexValidator(
                regex=r'^(?:\+7|8)\d{10}$',
                message='Введите номер в формате +71234567890 или 89123456789'
            )
        ],
        max_length=12,
        blank=True
    )

    class Meta:
        verbose_name = 'Клиент бота'
        verbose_name_plural = 'Клиенты бота'

    def __str__(self):
        return f'{self.telegram_id}'


class Cart(BaseModel):
    customer = models.OneToOneField(
        CustomerBot,
        verbose_name='Клиент',
        on_delete=models.CASCADE,
        related_name='cart'
    )
    payment_method = models.CharField(
        'Способ оплаты',
        choices=PaymentMethod,
        default=PaymentMethod.ROBOKASSA,
        max_length=10
    )
    comment = models.TextField(
        'Комментарий для заказа',
        blank=True,
        default=''
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'{self.customer}'

    @property
    def payment_method_display(self):
        return dict(PaymentMethod.choices).get(self.payment_method)

    @property
    def total_price(self) -> int:
        return sum(
            (item.product.price * item.quantity for item in self.items.all())
        )


class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart,
        verbose_name='Клиент',
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.PROTECT,
        related_name='cartitems'
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество',
        default=1
    )

    class Meta:
        verbose_name = 'Товар корзины'
        verbose_name_plural = 'Товары корзин'

    def __str__(self):
        return f'{self.product}'
