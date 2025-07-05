from django.conf import settings

from .base import APIClientBase


class OrderApi(APIClientBase):
    def __init__(self):
        super().__init__()
        self.base_url += '/order'

    def create_order(self, data: dict) -> dict:
        if settings.IS_TEST:
            self.params['test'] = 'on'
        response = self._post(url='/', data=data)
        return response.json()
