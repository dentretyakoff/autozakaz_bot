from .base import APIClientBase


class OrdersApi(APIClientBase):
    def __init__(self):
        super().__init__()
        self.base_url += '/orders'

    def get_orders(self, telegram_id: int) -> dict:
        response = self._get(f'/orders/?telegram_id={telegram_id}')
        return response.json()

    def get_order(self, pk: int) -> dict:
        response = self._get(f'/orders/{pk}')
        return response.json()

    def create_order(self, telegram_id: int) -> dict:
        response = self._post({'telegram_id': telegram_id}, '/orders/')
        return response.json()

    def cancel_order(self, order_id: int) -> dict:
        response = self._patch({}, f'/orders/{order_id}/cancel/')
        return response.json()
