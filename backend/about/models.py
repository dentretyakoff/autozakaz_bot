from django.db import models

from base.models import BaseModel


class Contact(BaseModel):
    requisites = models.TextField(
        max_length=2500,
        verbose_name='Реквизиты',
    )
    address = models.CharField(
        max_length=300,
        verbose_name='Адрес'
    )
    phone = models.CharField(
        max_length=100,
        verbose_name='Телефон'
    )
    email = models.EmailField(
        verbose_name='Почта'
    )
    is_actual = models.BooleanField(
        default=False,
        verbose_name='Актуален'
    )

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.address


class Oferta(BaseModel):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование'
    )
    text = models.TextField(
        max_length=2500,
        verbose_name='Текст',
    )
    is_actual = models.BooleanField(
        default=False,
        verbose_name='Актуальна'
    )
    oferta_file = models.FileField(
        upload_to='oferta_files/',
        blank=True,
        null=True,
        verbose_name='Файл'
    )

    class Meta:
        verbose_name = 'Оферта'
        verbose_name_plural = 'Оферта'

    def __str__(self):
        return self.name
