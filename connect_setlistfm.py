from base.client import SetlistRequests
from base.settings import ApiKeys

api_key = ApiKeys.SETLIST_FM

api = SetlistRequests()

result = api.get("/1.0/artist/0bfba3d3-6a04-4779-bb0a-df07df5b0558")
print(result)
