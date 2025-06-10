import re

from core.constants import QUERY_PATTERN, InputValidationConstants
from core.exceptions.validations import ValidationError


def validate_search_query(query: str) -> str:
    """Проверяет коректность поискового запроса."""
    query = query.strip()
    if not re.match(QUERY_PATTERN, query):
        raise ValidationError(InputValidationConstants.BAD_QUERY)
    return query
