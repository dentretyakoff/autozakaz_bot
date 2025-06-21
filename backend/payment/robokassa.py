import hashlib
import json
from decimal import Decimal, ROUND_DOWN
from datetime import datetime
from urllib import parse
from urllib.parse import urlparse

from django.conf import settings


def calculate_signature(*args) -> str:
    """Create signature MD5.
    """
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()


def parse_response(request: str) -> dict:
    """
    :param request: Link.
    :return: Dictionary.
    """
    params = {}

    for item in urlparse(request).query.split('&'):
        key, value = item.split('=')
        params[key] = value
    return params


def check_signature_result(
    order_number: int,  # invoice number
    received_sum: Decimal,  # cost of goods, RU
    received_signature: hex,  # SignatureValue
    password: str  # Merchant password
) -> bool:
    signature = calculate_signature(received_sum, order_number, password)
    if signature.lower() == received_signature.lower():
        return True
    return False


# Формирование URL переадресации пользователя на оплату.

def generate_payment_link(
    merchant_login: str,  # Merchant login
    merchant_password_1: str,  # Merchant password
    cost: Decimal,  # Cost of goods, RU
    number: int,  # Invoice number
    # description: str,  # Description of the purchase
    expiration_date: datetime,
    receipt: dict,
    is_test=0,
    robokassa_payment_url='https://auth.robokassa.ru/Merchant/Index.aspx',
) -> str:
    """URL for redirection of the customer to the service.
    """
    receipt_json = json.dumps(receipt, ensure_ascii=False)
    receipt_encoded = parse.quote(receipt_json)
    signature = calculate_signature(
        merchant_login,
        cost,
        number,
        receipt_encoded,
        merchant_password_1
    )

    data = {
        'MerchantLogin': merchant_login,
        'OutSum': cost,
        'InvId': number,
        # 'Description': description,
        'Receipt': receipt_encoded,
        'SignatureValue': signature,
        'IsTest': is_test,
        'ExpirationDate': expiration_date,
    }
    return f'{robokassa_payment_url}?{parse.urlencode(data)}'


# Получение уведомления об исполнении операции (ResultURL).

def result_payment(merchant_password_2: str, request: str) -> str:
    """Verification of notification (ResultURL).
    :param request: HTTP parameters.
    """
    param_request = parse_response(request)
    cost = param_request['OutSum']
    number = param_request['InvId']
    signature = param_request['SignatureValue']


    if check_signature_result(number, cost, signature, merchant_password_2):  # noqa
        return f'OK{param_request["InvId"]}'
    return "bad sign"


# Проверка параметров в скрипте завершения операции (SuccessURL).

def check_success_payment(merchant_password_1: str, request: str) -> str:
    """ Verification of operation parameters ("cashier check")
    in SuccessURL script.
    :param request: HTTP parameters
    """
    param_request = parse_response(request)
    cost = param_request['OutSum']
    number = param_request['InvId']
    signature = param_request['SignatureValue']


    if check_signature_result(number, cost, signature, merchant_password_1):  # noqa
        return "Thank you for using our service"
    return "bad sign"


def generate_payment_params(order):
    """Генерирует параметры для формы с POST запросом."""
    receipt = build_receipt(order)
    params = {
        'MerchantLogin': settings.MERCHANT_LOGIN,
        'OutSum': order.total_price,
        'InvId': str(order.id),
        'IsTest': settings.IS_TEST,
        'ExpirationDate': order.expiration_date,
        'Receipt': receipt
    }
    params['SignatureValue'] = calculate_signature(
        settings.MERCHANT_LOGIN,
        order.total_price,
        order.id,
        receipt,
        settings.MERCHANT_PASSWORD_1
    )
    return params


def build_receipt(order):
    items = []
    for item in order.items.all():
        items.append({
            'name': item.product.name,
            'quantity': item.quantity,
            'sum': to_robokassa_sum(item.price * item.quantity),
            'tax': 'none'
        })
    receipt = {'items': items}
    receipt_json = json.dumps(receipt, ensure_ascii=False)
    receipt_encoded = parse.quote(receipt_json)
    return receipt_encoded


def to_robokassa_sum(value):
    return float(Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_DOWN))
