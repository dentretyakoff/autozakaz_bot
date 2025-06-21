from requests.exceptions import HTTPError

from .base import APIClientBase


class UsersApi(APIClientBase):
    def __init__(self):
        super().__init__()
        self.base_url += '/users'

    def get_user(self, telegram_id: int) -> dict:
        return self._get(f'/bot-customers/{telegram_id}/')

    def create_or_update(self, telegram_id: int, nickname: str) -> list:
        try:
            response = self._post(
                data={'telegram_id': telegram_id, 'nickname': nickname},
                url='/bot-customers/'
            )
            return response.json()
        except HTTPError as e:
            if e.response.status_code == 400:
                response = self._patch(
                    data={'nickname': nickname},
                    url=f'/bot-customers/{telegram_id}/'
                )
            else:
                raise
            return response.json()

    def gdpr_confirm(self, telegram_id: int) -> dict:
        return self._patch(
            data={'gdpr_accepted': True},
            url=f'/bot-customers/{telegram_id}/'
        )

    def get_cart(self, telegram_id: int) -> dict:
        return self._get(f'/cart/{telegram_id}/').json()

    def add_product(self, data: dict):
        self._post(data=data, url='/cart-items/')

    def delete_cartitem(self, cartitem_id: int):
        self._delete(f'/cart-items/{cartitem_id}/')

    def update_phone(self, telegram_id: int, phone: str) -> dict:
        return self._patch(
            data={'phone': phone},
            url=f'/bot-customers/{telegram_id}/'
        )

    def update_comment(self, telegram_id: int, comment: str) -> dict:
        return self._patch(
            data={'comment': comment},
            url=f'/cart/{telegram_id}/'
        )
