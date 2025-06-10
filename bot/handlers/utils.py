import logging

from aiogram.types import Message, CallbackQuery

from core.constants import MessagesConstants

logger = logging.getLogger(__name__)


def make_message_contacts(contacts: dict) -> str:
    """Подготоавливает сообщение с контактами."""
    if not contacts:
        return MessagesConstants.CONTACTS

    text = ''
    for contact in contacts.values():
        text += contact
        text += '\n\n'

    return text


async def delete_previous_message(
        message_id: int,
        message: Message | CallbackQuery = None) -> None:
    try:
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=message_id)
    except Exception as e:
        logging.error(f'Ошибка удаления сообщения: {e}')
