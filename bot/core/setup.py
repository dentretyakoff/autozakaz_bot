from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from handlers.common import router as common_router
from handlers.errors import router as errors_router
from handlers.contacts import router as contacts_router
from handlers.products import router as products_router
from .constants import CommandConstants


async def setup_bot_commands(bot: Bot) -> None:
    """Установка команд для бота.
    Args:
        bot: Экземпляр бота.
    """
    commands = [
        BotCommand(command='start', description=CommandConstants.start)
    ]
    await bot.set_my_commands(commands)


def setup_routers(dispatcher: Dispatcher) -> None:
    """Регистрация роутеров.
    Args:
        dispatcher: Экземпляр диспетчера.
    """
    dispatcher.include_router(common_router)
    dispatcher.include_router(errors_router)
    dispatcher.include_router(contacts_router)
    dispatcher.include_router(products_router)
