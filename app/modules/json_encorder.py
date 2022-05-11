from bson.objectid import ObjectId
from json import JSONEncoder

class CustomJsonEncorder(JSONEncoder):
    def default(self, obj):
        # ObjectId -> str
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return super().default(self, obj)