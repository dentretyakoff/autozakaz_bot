from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .enums import LogLevel


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        'Создан',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Изменен',
        auto_now=True
    )

    class Meta:
        abstract = True


class BaseLogModel(BaseModel):
    level = models.CharField(
        'Уровень',
        max_length=10,
        choices=LogLevel,
        default=LogLevel.INFO
    )
    message = models.TextField(
        max_length=3000,
        verbose_name='Сообщение'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Тип объекта'
    )
    object_id = models.PositiveIntegerField('ID объекта')
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
        ordering = ('-created_at',)
