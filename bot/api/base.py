import requests
from requests import Response

from core import settings


class APIClientBase:
    def __init__(self):
        self.base_url = settings.BACKEND_URL.rstrip('/') + '/api/v1'
        self.token = settings.API_TOKEN
        self.headers = {'Authorization': f'Token {self.token}'}

    def _get(self, url) -> Response:
        response = requests.get(url=self.base_url + url, headers=self.headers)
        response.raise_for_status()
        return response

    def _post(self, data: dict, url: str) -> Response:
        self.headers['Content-Type'] = 'application/json'
        response = requests.post(
            url=self.base_url + url,
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response

    def _patch(self, data: dict, url: str) -> Response:
        self.headers['Content-Type'] = 'application/json'
        response = requests.patch(
            url=self.base_url + url,
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response

    def _delete(self, url: str) -> None:
        requests.delete(url=self.base_url + url, headers=self.headers)
