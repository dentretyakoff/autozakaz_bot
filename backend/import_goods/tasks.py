import logging

from django.utils import timezone

from core import celery_app
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
        downloader = CSVImport(csv_price=price)
        downloader.import_csv()
        logger.info(f'Прайс {price.name} загружен.')
    task.last_run = timezone.localtime()
    task.save(update_fields=['last_run'])
