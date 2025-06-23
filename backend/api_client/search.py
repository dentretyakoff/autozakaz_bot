from .base import APIClientBase


class SearchApi(APIClientBase):
    def __init__(self):
        super().__init__()
        self.base_url += '/search'

    def q(self, q: str) -> dict:
        self.params['q'] = q
        response = self._get('/')
        return response.json()
