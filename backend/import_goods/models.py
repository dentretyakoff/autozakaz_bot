from django.db import models

from base.models import BaseModel


class CSVPrice(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование'
    )
    url = models.URLField(
        verbose_name='Путь к файлу для скачивания',
        help_text='Пример: https://example.ru/media/pricelist_n398.csv'
    )

    class Meta:
        verbose_name = 'Прайс поставщика'
        verbose_name_plural = 'Прайсы поставщиков'

    def __str__(self):
        return f'Прайс поставщика: - {self.name}'


class ImportTask(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование'
    )
    run_at = models.TimeField(
        verbose_name='Время запуска'
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Включена'
    )
    scheduled_at = models.DateTimeField(
        verbose_name='Запущена',
        null=True,
        blank=True
    )
    last_run = models.DateTimeField(
        verbose_name='Завершена',
        null=True,
        blank=True
    )
    prices = models.ManyToManyField(
        CSVPrice,
        verbose_name='Прайсы',
        related_name='tasks'
    )

    class Meta:
        verbose_name = 'Задача импорта'
        verbose_name_plural = 'Задачи импорта'

    def __str__(self):
        return f'Задача - {self.name}'

    def should_schedule_now(self, now, delay):
        if not self.active:
            return False

        if self.scheduled_at and self.scheduled_at.date() == now.date():
            return False

        return 0 <= delay <= 300
