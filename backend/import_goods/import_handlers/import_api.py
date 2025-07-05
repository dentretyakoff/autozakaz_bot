import logging
from decimal import Decimal

from products.models import Product
from api_client import api_supplier
from .base import ImportBase


logger = logging.getLogger(__name__)


class APIImport(ImportBase):
    def __init__(self):
        super().__init__()
        self.api = api_supplier

    def prepare_product(self, data: dict, product: Product) -> dict | None:
        """
        Обрабатывает найденные товары, отбрасывает аналоги, убирает дубли.
        """
        items = [
            item for item in data.get('objects', [])
            if item.get('code') == product.code and
               item.get('maker') == product.manufacturer.name  # noqa
        ]
        if not items:
            return None

        min_period = min(item['period_min'] for item in items)
        candidates = [
            item for item in items if item['period_min'] == min_period
        ]
        best = min(candidates, key=lambda x: Decimal(x['price']))

        return best

    def update_products(self, qs):
        """Актуализирует цену и срок."""
        updated_products = []
        is_published_products = []
        unpublished_products = []

        try:
            for product in qs:
                result = self.api.search.q(product.code)
                product_data = self.prepare_product(result, product)

                if product_data:
                    price = product_data['price']
                    product.price = self.increase_price(Decimal(price))
                    product.period_min = product_data['period_min']
                    product.min_qty = product_data['min_qty']
                    product.qty = product_data['qty']
                    product.is_published = True
                    is_published_products.append(product)
                else:
                    product.is_published = False
                    unpublished_products.append(product)
                updated_products.append(product)
            Product.objects.bulk_update(
                updated_products,
                fields=['price', 'is_published',
                        'period_min', 'min_qty', 'qty']
            )
            qs = Product.objects.filter(
                pk__in=[p.pk for p in is_published_products])
            return qs, unpublished_products
        except Exception as e:
            logger.error(f'Ошибка актуализации цен по api: {e}')
            return Product.objects.none(), unpublished_products
