from requests.exceptions import HTTPError

from .base import APIClientBase


class UsersApi(APIClientBase):
    def __init__(self):
        super().__init__()
        self.base_url += '/users'

    def get_user(self, telegram_id: int):
        return self._get(f'/bot-customers/{telegram_id}/')

    def create_or_update(self, telegram_id: int, nickname: str) -> list:
        try:
            response = self._post(
                data={'telegram_id': telegram_id, 'nickname': nickname},
                url='/bot-customers/'
            )
            return response.json().get('results')[0]
        except HTTPError as e:
            if e.response.status_code == 400:
                response = self._patch(
                    data={'nickname': nickname},
                    url=f'/bot-customers/{telegram_id}/'
                )
            else:
                raise
            return response.json()

    def gdpr_confirm(self, telegram_id: int):
        return self._patch(
            data={'gdpr_accepted': True},
            url=f'/bot-customers/{telegram_id}/'
        )
