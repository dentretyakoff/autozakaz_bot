from .settings import PROJECT_NAME


class MessagesConstants:
    ERROR = '🤷 Извините, бот сейчас не доступен, пожалуйста попробуйте позже.'
    HELLO = (
        f'Добро пожаловать в {PROJECT_NAME}'
    )
    UNKNOWN_COMMAND = (
        '❔ Кажется, я не понял твое сообщение. '
        'Попробуй ввести другую команду или уточнить, '
        'что ты хотел сделать.'
    )
    CONTACTS = 'Контакты скоро появятся'
    START_SEARCH = 'Введи код производителя или артикул товара:'
    WAITING_SEARCH = '💭 Принял код, произвожу поиск...'
    NOT_FOUND = 'По запросу ничего не найдено, попробуй еще раз'


class CommandConstants:
    start = 'Начать работу с чат-ботом.'


MAX_QUERY_LEN = 20
QUERY_PATTERN = rf'^[A-Za-z0-9]{{1,{MAX_QUERY_LEN}}}$'


class InputValidationConstants:
    BAD_QUERY = ('Некорректный запрос, допускаются цифры от 0 до 9 и букы '
                 f'латинского алфавита. Максимальная длинна {MAX_QUERY_LEN} '
                 'символов.')
