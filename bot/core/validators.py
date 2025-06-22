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


def validate_search_query(query: str) -> str:
    """Проверяет коректность поискового запроса."""
    query = query.strip()
    if not re.match(QUERY_PATTERN, query):
        raise ValidationError(InputValidationConstants.BAD_QUERY)
    return query


def validate_quantity_is_number(quantity: str) -> str:
    """Проверяет является ли количество положительным числом."""
    if not quantity.isdigit() or not (MIN_QUANTITY <= int(quantity) <= MAX_QUANTITY):  # noqa
        raise ValidationError(InputValidationConstants.INCORRECT_QUANTITY)
    return quantity


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
