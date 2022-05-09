import time

import requests
from requests.structures import CaseInsensitiveDict

from .settings import ApiKeys, ApiURLS

apikeys = ApiKeys()
apiurls = ApiURLS()


class BaseRequests:
    HEADERS = CaseInsensitiveDict()

    def __init__(self):
        self.HEADERS["Accept"] = "application/json"
        self.HEADERS["Content-Type"] = "application/json"

    def get(self, *args, **kwargs):
        return requests.get(*args, **kwargs).json()


class SetlistRequests(BaseRequests):
    def __init__(self):
        super(SetlistRequests, self).__init__()
        self.HEADERS["x-api-key"] = apikeys.SETLIST_FM

    def get(self, path, *args, **kwargs):
        url = apiurls.SETLIST_FM
        if path[0] != "/":
            url += "/"
        url += path
        time.sleep(0.5)
        return super().get(url, headers=self.HEADERS, *args, **kwargs)


class SpotifyRequests(BaseRequests):
    pass


class MusicbrainzRequests(BaseRequests):
    pass
