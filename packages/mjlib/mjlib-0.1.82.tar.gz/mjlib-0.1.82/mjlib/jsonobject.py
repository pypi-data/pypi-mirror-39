import json


class JsonObject:
    def __init__(self, j=None):
        if j is not None:
            self.__dict__ = json.loads(j)
