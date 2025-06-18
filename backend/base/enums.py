from django.db import models


class LogLevel(models.TextChoices):
    INFO = 'INFO', 'Информация'
    WARNING = 'WARNING', 'Предупреждение'
    ERROR = 'ERROR', 'Ошибка'
    DEBUG = 'DEBUG', 'Отладка'


class PaymentMethod(models.TextChoices):
    CASH = 'cash', 'Наличные'
    CARD = 'card', 'Карта'
    ROBOKASSA = 'robokassa', 'Робокасса'
