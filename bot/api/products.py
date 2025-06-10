from .base import APIClientBase


class ProductsApi(APIClientBase):
    def __init__(self):
        super().__init__()
        self.base_url += '/products'

    def search_products(self, query: str) -> list:
        response = self._get(f'/products/?search={query}')
        results = response.json()['results']
        return results
