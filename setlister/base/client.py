import requests
from requests.structures import CaseInsensitiveDict
from setlister.settings import ApiKeys, ApiURLS

apikeys = ApiKeys()
apiurls = ApiURLS()


class BaseAPI:
    HEADERS = CaseInsensitiveDict()

    def __init__(self):
        self.HEADERS["Accept"] = "application/json"
        self.HEADERS["Content-Type"] = "application/json"

    def get(self, *args, **kwargs):
        return requests.get(*args, **kwargs).json()

    def post(self, *args, **kwargs):
        return requests.post(*args, **kwargs).json()
