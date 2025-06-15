from django.db import models

from base.models import BaseModel


class CustomerBot(BaseModel):
    telegram_id = models.PositiveBigIntegerField(
        'Телеграм ID',
        unique=True
    )
    nickname = models.CharField(
        'Никнейм',
        null=True,
        blank=True,
        max_length=255
    )
    gdpr_accepted = models.BooleanField(
        default=False,
        verbose_name='Согласие на ПД',
        help_text='Статус согласия на обработку перс. данных'
    )

    class Meta:
        verbose_name = 'Клиент бота'
        verbose_name_plural = 'Клиенты бота'

    def __str__(self):
        return f'{self.telegram_id}'
