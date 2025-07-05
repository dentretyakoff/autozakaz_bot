import logging

from api_client import api_supplier
from core import celery_app
from import_goods.import_handlers.import_api import APIImport
from .models import Order


logger = logging.getLogger(__name__)


@celery_app.task
def create_orders(order_id: int):
    """Создает заказы у поставщика."""
    order = Order.objects.get(pk=order_id)
    order_items = order.items.all()
    service = APIImport()
    for order_item in order_items:
        try:
            result = api_supplier.search.q(order_item.product.code)
            product_data = service.prepare_product(result, order_item.product)

            if product_data:
                product_data['order_qty'] = order_item.quantity
                product_data['client_comment'] = str(order.pk)
                response = api_supplier.order.create_order(product_data)
                comment = response.get('number') or response.get('error')
            else:
                comment = 'Товар не найден у поставщика.'
        except Exception as e:
            logger.exception(f'Ошибка при обработке позиции {order_item.pk}')
            comment = f'Ошибка: {e}'
        order_item.comment = comment
        order_item.save()
