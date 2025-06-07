import logging
import time

from django.utils import timezone

from core import celery_app
from base.enums import LogLevel
from .models import ImportTask
from .import_csv import CSVImport


logger = logging.getLogger(__name__)


@celery_app.task
def check_scheduled_tasks():
    tasks = ImportTask.objects.filter(active=True)
    now = timezone.localtime()
    for task in tasks:
        run_time = now.replace(
            hour=task.run_at.hour,
            minute=task.run_at.minute,
            second=task.run_at.second,
        )
        delay = (run_time - now).total_seconds()
        if task.should_schedule_now(now=now, delay=delay):
            import_goods.apply_async(args=[task.id], countdown=delay)
            task.scheduled_at = run_time
            task.save(update_fields=['scheduled_at'])


@celery_app.task
def import_goods(task_id: int):
    task = ImportTask.objects.get(id=task_id)
    logger.info(f'Запущена задача скачивания прайс-листов: {task.name}')
    prices = task.prices.all()
    for price in prices:
        message = f'{price.name} - Начат импорт товаров'
        logger.info(message)
        price.logs.create(level=LogLevel.INFO, message=message)
        start_time = time.time()
        downloader = CSVImport(csv_price=price)
        try:
            downloader.import_csv()
            duration = time.time() - start_time
            message = f'{price.name} - ✅ импорт завершен за {duration:.4f} сек.'  # noqa
            logger.info(message)
            price.logs.create(level=LogLevel.INFO, message=message)
        except Exception:
            message = f'{price.name} - ❌ импорт прерван.'
            logger.info(message)
            price.logs.create(level=LogLevel.ERROR, message=message)
    task.last_run = timezone.localtime()
    task.save(update_fields=['last_run'])
