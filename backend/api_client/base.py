import requests
from requests import Response

from django.conf import settings


class APIClientBase:
    def __init__(self):
        self.base_url = settings.API_SUPPLIER.rstrip('/') + '/v1'
        self.token = settings.API_TOKEN_SUPPLIER
        self.params = {'api_key': self.token}

    def _get(self, url) -> Response:
        response = requests.get(url=self.base_url + url, params=self.params)
        response.raise_for_status()
        return response
