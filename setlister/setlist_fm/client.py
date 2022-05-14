import time

from base.client import BaseAPI
from setlister.settings import ApiKeys, ApiURLS

apikeys = ApiKeys()
apiurls = ApiURLS()


class SetlistAPI(BaseAPI):
    def __init__(self):
        super(SetlistAPI, self).__init__()
        self.HEADERS["x-api-key"] = apikeys.SETLIST_FM

    def get(self, path, *args, **kwargs):
        url = apiurls.SETLIST_FM
        if path[0] != "/":
            url += "/"
        url += path
        time.sleep(0.5)
        return super().get(url, headers=self.HEADERS, *args, **kwargs)


class MusicbrainzAPI(BaseAPI):
    def __init__(self):
        super(MusicbrainzAPI, self).__init__()
        self.HEADERS["User-Agent"] = apikeys.MUSICBRAINZ

    def get(self, path, *args, **kwargs):
        url = apiurls.MUSICBRAINZ
        if path[0] != "/":
            url += "/"
        url += path
        return super().get(url, headers=self.HEADERS, *args, **kwargs)
