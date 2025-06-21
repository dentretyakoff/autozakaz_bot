from django.db import models


class OrderStatus(models.TextChoices):
    AWAITING = 'awaiting', 'Ожидает'
    CANCELLED = 'cancelled', 'Отменен'
    PAID = 'paid', 'Оплачен'
