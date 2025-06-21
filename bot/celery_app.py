import time
import logging
import asyncio

from celery import Celery

from core import settings
from api import api_backend
from core.constants import MessagesConstants, OrderStatus
from handlers.utils import get_order_detail
from core.bot_instance import bot


logger = logging.getLogger(__name__)


celery_app = Celery(
    'celery_app',
    broker=f'redis://{settings.REDIS_HOST}:6379/0',
    backend=f'redis://{settings.REDIS_HOST}:6379/0'
)
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.task_default_queue = 'bot'


@celery_app.task
def check_payment(order_id, user_id, start_time, attempt=1):
    """
    Проверяем оплату каждые settings.INTERVAL_CHECK_PAYMENT сек.
    Максимум settings.MAX_CHECK_PAYMENT_TIME минут.
    """
    logger.info(f'Оплата заказа: {order_id}, пользователь {user_id}, '
                f'попытка № {attempt}')
    elapsed_time = time.time() - start_time
    loop = asyncio.get_event_loop()
    order = api_backend.orders.get_order(order_id)

    if order.get('status') == OrderStatus.CANCELLED:
        return  # Прекращаем проверки

    if elapsed_time > settings.MAX_CHECK_PAYMENT_TIME:
        api_backend.orders.cancel_order(order_id)
        loop.run_until_complete(bot.send_message(
            chat_id=user_id,
            text=MessagesConstants.PAYMENT_NOT_RECEIVED))
        logger.info(f'Отменен заказ: {order_id}, пользователь {user_id}')
        return  # Прекращаем проверки

    if order.get('status') == OrderStatus.PAID:
        text = get_order_detail(order)
        loop.run_until_complete(bot.send_message(
            chat_id=user_id,
            text=f'{MessagesConstants.PAYMENT_OK}'))
        loop.run_until_complete(bot.send_message(
            chat_id=settings.GROUP_ID,
            text=text))
    else:
        attempt += 1
        check_payment.apply_async(
            (order_id, user_id, start_time, attempt),
            countdown=settings.INTERVAL_CHECK_PAYMENT)


def start_payment_check(order_id, user_id):
    """Запуск первой задачи с отметкой времени старта."""
    start_time = time.time()
    logger.info(f'Старт проверки оплаты - заказ: {order_id}, '
                f'пользователь - {user_id}')
    check_payment.apply_async(
        (order_id, user_id, start_time),
        countdown=settings.INTERVAL_CHECK_PAYMENT
    )
