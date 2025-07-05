import re

from aiogram.types import Message

from core.constants import (
    QUERY_PATTERN,
    MAX_QUANTITY,
    MIN_QUANTITY,
    InputValidationConstants,
    PHONE_PATTERN
)
from core.exceptions.validations import ValidationError
from .utils import parse_max_quantity


def validate_search_query(query: str) -> str:
    """Проверяет коректность поискового запроса."""
    query = query.strip()
    if not re.match(QUERY_PATTERN, query):
        raise ValidationError(InputValidationConstants.BAD_QUERY)
    return query


def validate_phone_number(phone: str) -> str:
    """Проверяет номер телефона клиента."""
    if not re.match(PHONE_PATTERN, phone.strip()):
        raise ValidationError(InputValidationConstants.INCORRECT_PHONE_NUMBER)
    return phone.strip()


def validate_message_is_text(message: Message) -> str:
    """Валидация является ли сообщение текстовым."""
    if message.content_type != 'text':
        raise ValidationError(InputValidationConstants.MESSAGE_IS_NOT_TEXT)
    return message.text


def validate_quantity(quantity: str, product: dict) -> int:
    """Валидация кратности и доступному количеству на складе."""
    if not quantity.isdigit() or not (MIN_QUANTITY <= int(quantity) <= MAX_QUANTITY):  # noqa
        raise ValidationError(InputValidationConstants.INCORRECT_QUANTITY)

    quantity = int(quantity)
    min_qty = product.get('min_qty') or MIN_QUANTITY

    if quantity % min_qty != 0:
        message = ('Не соответствует минимальному количеству\n'
                   f'Введите {min_qty} или {min_qty * 2} или '
                   f'{min_qty * 3} и т.д.')
        raise ValidationError(message)

    qty = product.get('qty') or '-'
    limit_type, max_value = parse_max_quantity(qty)

    if limit_type == 'lt' and not (quantity < max_value):
        raise ValidationError(f'Можно заказать меньше {max_value} шт.')

    elif limit_type == 'max' and quantity > max_value:
        raise ValidationError(f'Можно заказать не более {max_value} шт.')

    return quantity
