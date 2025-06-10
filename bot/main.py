import asyncio
import logging

from aiogram import Dispatcher

from core import settings
from core.setup import setup_bot_commands, setup_routers
from core.bot_instance import bot


logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.ERROR,
    format='%(asctime)s - [%(levelname)s] - %(name)s - '
           '%(filename)s.%(funcName)s(%(lineno)d) - %(message)s')


async def main():
    """Запуск бота."""
    dispatcher = Dispatcher()
    dispatcher.startup.register(setup_bot_commands)
    dispatcher.startup.register(setup_routers)

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
