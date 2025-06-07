from django.db import models

from base.models import BaseModel, BaseLogModel
from base.managers import get_specific_content_type_manager
from django.contrib.contenttypes.fields import GenericRelation


class CSVPrice(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование'
    )
    url = models.URLField(
        verbose_name='Путь к файлу для скачивания',
        help_text='Пример: https://example.ru/media/pricelist_n398.csv'
    )
    period_min = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Фильтр по "Срок мин"',
        help_text=('Оставит детали со "Срок мин" равные или '
                   'больше указанного значения')
    )
    new_period_min = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Новый "Срок мин"',
        help_text=('Переназначит у всех деталей "Срок мин", '
                   'если указано больше 0.')
    )
    price_filter = models.FloatField(
        default=0,
        verbose_name='Фильтр по цене',
        help_text=('Оставит детали где "Цена" больше или '
                   'равна указанному значению')
    )
    ignored_manufacturers = models.ManyToManyField(
        'products.Manufacturer',
        verbose_name='Фильтр по производителям',
        blank=True,
        related_name='ignored_in_prices'
    )
    logs = GenericRelation('CsvImportLog')

    class Meta:
        verbose_name = 'Прайс поставщика'
        verbose_name_plural = 'Прайсы поставщиков'

    def __str__(self):
        return self.name


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

        # Планируем запуск задачи если delay в пределах 5 минут
        return 0 <= delay <= 300


class CSVColumn(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование'
    )
    drop_by_words = models.BooleanField(
        default=False,
        verbose_name='Удаление по словам',
        help_text='Столбец будет учитываться при удалении по словам'
    )

    class Meta:
        verbose_name = 'Столбец в прайсе'
        verbose_name_plural = 'Столбцы в прайсах'

    def __str__(self):
        return self.name


class WordToDrop(BaseModel):
    word = models.CharField(
        max_length=100,
        verbose_name='Слово'
    )

    class Meta:
        verbose_name = 'Слово для удаления'
        verbose_name_plural = 'Слова для удаления'

    def __str__(self):
        return self.word


class CsvImportLog(BaseLogModel):
    """Лог для импорта прайс-листа."""
    objects = get_specific_content_type_manager(CSVPrice)

    class Meta:
        verbose_name = 'Лог импорта'
        verbose_name_plural = 'Логи импорта'

    def __str__(self):
        return self.message[:30]
