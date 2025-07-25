import string

from django.db import models
from django_meili.models import IndexMixin

from base.models import BaseModel


class Manufacturer(BaseModel):
    name = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name='Наименование',
        unique=True
    )

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Product(IndexMixin, BaseModel):
    manufacturer = models.ForeignKey(
        Manufacturer,
        verbose_name='Производитель',
        on_delete=models.CASCADE
    )
    code = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name='Код'
    )
    name = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name='Наименование'
    )
    description = models.TextField(
        max_length=2500,
        verbose_name='Описание',
        null=True,
        blank=True
    )
    price = models.PositiveBigIntegerField(
        verbose_name='Цена',
        null=True,
        blank=True
    )
    period_min = models.CharField(
        max_length=150,
        verbose_name='Срок мин',
        null=True,
        blank=True
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликована',
        help_text='Если задан, товар будет отображаться на сайте'
    )
    product_code = models.CharField(
        max_length=6,
        verbose_name='Артикул товара',
        db_index=True,
        blank=True,
        null=True
    )
    min_qty = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Минимальное количество "min_qty"',
        help_text=('если min_qty = 2, то order_qty может '
                   'быть равен 2, или 4, или 8, и т.д.')
    )
    qty = models.CharField(
        null=True,
        blank=True,
        verbose_name='Доступно для заказа'
    )

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('manufacturer', 'code'),
                name='unique_product_per_csv')
        ]

    class MeiliMeta:
        searchable_fields = ('code', 'product_code')
        filterable_fields = ('is_published',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_published = self.is_published

    def __str__(self):
        return f'{self.name}: {self.code}'

    def meili_filter(self):
        return self.is_published

    def save(self, *args, **kwargs):
        should_remove = self.pk and self._is_published and not self.is_published  # noqa
        super().save(*args, **kwargs)
        if should_remove:
            self.meilisearch.index.delete_document(str(self.pk))
        self._is_published = self.is_published

    def id_to_base36(self, num: int, min_length: int = 6) -> str:
        chars = string.digits + string.ascii_uppercase
        if num == 0:
            return chars[0].rjust(min_length, '0')
        result = ''
        while num > 0:
            num, rem = divmod(num, 36)
            result = chars[rem] + result
        return result.rjust(min_length, '0')


class PriceMarkup(BaseModel):
    threshold = models.PositiveBigIntegerField(
        verbose_name='Порог цены',
        unique=True
    )
    percent = models.FloatField(verbose_name='Процент наценки')

    class Meta:
        ordering = ('threshold',)
        verbose_name = 'Коэфициент наценки'
        verbose_name_plural = 'Коэфиценты наценки'

    def __str__(self):
        return f'До {self.threshold} ₽ — +{self.percent}%'
