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
    CHOOSE_PRODUCT = 'Выбери деталь чтобы узнать подробнее'
    QUERY_EXPIRED = 'Поисковый запрос не найден'
    DEFAULT_GDPR = (
        'Необходимо согласие на обработку персональных данных:\n'
        ' - Telegram ID и ник (для связи)\n'
        ' - Номер телефона (для подтверждения заказа)\n'
        ' - Адрес доставки (если требуется)\n'
        'Днные используются только для выполнения заказа и '
        'не передаются третьим лицам.\n'
        'Нажмите «Cогласен», чтобы продолжить.'
    )
    REQUEST_COMMENT = 'Укажи адрес доставки и комментарий к заказу'
    PAY_ORDER = (
        '👍 Заказ оформлен.\n'
        'Для перехода к оплате нажмите кнопку "Оплатить".\n'
        'Спасибо.'
    )
    PAYMENT_NOT_RECEIVED = '❌ Оплата не поступила, заказ отменён.'
    PAYMENT_OK = '✅ Оплата подтверждена!'


class CommandConstants:
    start = 'Начать работу с чат-ботом.'


class OrderStatus:
    PAID = 'paid'
    AWAITING = 'awaiting'
    CANCELLED = 'cancelled'

    ICONS = {
        PAID: '✅',
        AWAITING: '⏳',
        CANCELLED: '❌',
    }
    ICONS_WITH_TEXT = {
        PAID: '✅ Оплачен',
        AWAITING: '⏳ Ожидает оплаты',
        CANCELLED: '❌ Отменен',
    }

    @classmethod
    def get_icon(cls, status: str) -> str:
        return cls.ICONS.get(status, '❔')

    @classmethod
    def get_icon_with_text(cls, status: str) -> str:
        return cls.ICONS_WITH_TEXT.get(status, '❔')


MAX_LEN_DESCRIPTION = 500
MIN_QUANTITY = 1
MAX_QUANTITY = 32767
PHONE_PATTERN = r'^(?:\+7|8)\d{10}$'
MAX_QUERY_LEN = 30
QUERY_PATTERN = rf'^[A-Za-z0-9]{{1,{MAX_QUERY_LEN}}}$'


class InputValidationConstants:
    BAD_QUERY = ('Некорректный запрос, допускаются цифры от 0 до 9 и букы '
                 f'латинского алфавита. Максимальная длинна {MAX_QUERY_LEN} '
                 'символов.')
    INCORRECT_PHONE_NUMBER = (
        'Некорректный номер телефона.\n'
        'Пожалуйста введите в формате +71234567890 или 89123456789.'
    )
    MESSAGE_IS_NOT_TEXT = (
        'Вы отправили файл вместо текста, '
        'пожалуйста введите текстовое сообщение.'
    )
    INCORRECT_QUANTITY = f'Введите число от {MIN_QUANTITY} до {MAX_QUANTITY}'
