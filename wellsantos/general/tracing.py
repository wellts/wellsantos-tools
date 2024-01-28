from uuid import uuid4

from .model import Model


class ParentRequestId:
    def __init__(self, value=''):
        self.value = value or uuid4().hex

    def __str__(self):
        return self.value


class RequestId(ParentRequestId):
    pass


class RequestPayload(Model):
    pass


class ResponsePayload(Model):
    pass
