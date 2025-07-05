from .search import SearchApi
from .order import OrderApi


class API:
    def __init__(self):
        self.search = SearchApi()
        self.order = OrderApi()


api_supplier = API()
