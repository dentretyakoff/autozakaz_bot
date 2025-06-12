import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


DEBUG = os.getenv('DEBUG', 'false').lower() in ('true',)

TOKEN = os.getenv('TELEGRAM_TOKEN')

BACKEND_URL = os.getenv('BACKEND_API_URL')
API_TOKEN = os.getenv('BACKEND_API_TOKEN')

PROJECT_NAME = os.getenv('PROJECT_NAME', 'Project-Name')

# Robokassa
# Максимальное время для проверки оплаты (секунды)
MAX_CHECK_PAYMENT_TIME = int(os.getenv('MAX_CHECK_PAYMENT_TIME', 1800))
# Интервал проверки оплаты (секунды)
INTERVAL_CHECK_PAYMENT = int(os.getenv('INTERVAL_CHECK_PAYMENT', 30))
# Максимальный срок оплаты
ORDER_MAX_LIFE_TIME = int(os.getenv('EXPIRATION_DATE', 1200))

# Элементов на страницу
PAGE_SIZE = int(os.getenv('PAGE_SIZE', 10))
