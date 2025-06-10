from .base import APIClientBase


class AboutApi(APIClientBase):
    def __init__(self):
        super().__init__()
        self.base_url += '/about'

    def get_contacts(self) -> dict:
        response = self._get('/contacts/')
        results = response.json()['results']
        contacts = {}
        if len(results) > 0:
            contacts = results[0]
        return contacts
