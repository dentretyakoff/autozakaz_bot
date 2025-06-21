from http import HTTPStatus

from django.core.exceptions import PermissionDenied
from django.core import signing
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404, render

from base.enums import PaymentMethod
from payment.robokassa import generate_payment_params
from .models import Order


def robokassa_redirect(request, token):
    """Формирует форму для оплаты через робокассу."""
    try:
        order_id = signing.loads(token)
    except signing.BadSignature:
        raise PermissionDenied('Невалидный токен')
    order = get_object_or_404(Order, id=order_id)

    if order.payment_method != PaymentMethod.ROBOKASSA:
        raise PermissionDenied(
            'Заказ не предназначен для оплаты через Робокассу.')
    if order.expiration_date < timezone.now():
        return render(request, 'expired.html', status=HTTPStatus.BAD_REQUEST)

    params = generate_payment_params(order)
    context = {
        'robokassa_url': settings.ROBOKASSA_URL,
        'params': params,
    }
    return render(request, 'robokassa_redirect.html', context)
