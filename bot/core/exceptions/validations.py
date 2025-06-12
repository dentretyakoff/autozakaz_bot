"""Модуль исключений при валидации."""
from core.exceptions.base import BotError


class ValidationError(BotError):
    """Базовый класс для исключений при валидации."""
    def __init__(self, message: str):
        super().__init__(message)
