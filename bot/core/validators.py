import re

from core.constants import (
    QUERY_PATTERN,
    MAX_QUANTITY,
    MIN_QUANTITY,
    InputValidationConstants
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
