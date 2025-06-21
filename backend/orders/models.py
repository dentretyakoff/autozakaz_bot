from typing import Any
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone

from base.models import BaseModel
from base.enums import PaymentMethod
from users.models import CustomerBot
from products.models import Product
from .enums import OrderStatus


class Order(BaseModel):
    status = models.CharField(
        'Статус оплаты',
        choices=OrderStatus,
        max_length=10,
        blank=True,
        null=True
    )
    customer = models.ForeignKey(
        CustomerBot,
        verbose_name='Клиент',
        related_name='orders',
        on_delete=models.PROTECT
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
    expiration_date = models.DateTimeField(
        'Срок оплаты',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-id',)

    def __str__(self):
        return f'Заказ № {self.pk}'

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.pk and self.payment_method == PaymentMethod.ROBOKASSA:
            self.expiration_date = timezone.now() + timedelta(
                seconds=settings.ORDER_MAX_LIFE_TIME
            )
            self.status = OrderStatus.AWAITING
        return super().save(*args, **kwargs)

    @property
    def payment_method_display(self):
        return dict(PaymentMethod.choices).get(self.payment_method)

    @property
    def total_price(self) -> int:
        return sum(
            (item.price * item.quantity for item in self.items.all())
        )


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.CASCADE,
        related_name='orderitems'
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество',
        default=1
    )
    price = models.PositiveBigIntegerField(
        'Цена',
        help_text='Фиксируется в момент оформления заказа',
    )

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказов'

    def __str__(self):
        return f'{self.product}'
