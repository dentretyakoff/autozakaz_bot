from .search import SearchApi


class API:
    def __init__(self):
        self.search = SearchApi()


api_supplier = API()
