import logging

from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from core.constants import MessagesConstants, MAX_LEN_DESCRIPTION

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


def make_product_text(product: dict) -> str:
    """Подготавливает сообщение с деталями о товаре."""
    text = ''
    text += f'🏷 {product.get("name")}\n\n'
    text += f'🏭 Производитель: {product.get("manufacturer")}\n'
    text += f'🌐 Код: {product.get("code")}\n'
    text += f'🔤 Артикул: {product.get("product_code")}\n\n'
    description = product.get("description")
    if description:
        text += f'📖 Описание:\n{description[:MAX_LEN_DESCRIPTION]}\n\n'
    text += f'🕐 Срок доставки(рабочие дни): {product.get("period_min")}\n\n'
    text += f'💰 Цена: {product.get("price")} ₽\n'
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


async def safe_delete_message(message: Message) -> None:
    try:
        await message.delete()
    except TelegramBadRequest as e:
        text = str(e).lower()
        if "message can't be deleted for everyone" in text:
            logger.info('Не могу удалить старое сообщение.')
        else:
            logger.warning(f'Ошибка при удалении сообщения: {e}')
