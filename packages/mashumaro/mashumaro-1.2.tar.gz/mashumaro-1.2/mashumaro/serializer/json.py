import json
from typing import Union

from mashumaro.serializer.base import DataClassDictMixin


class DataClassJSONMixin(DataClassDictMixin):
    def to_json(self, encoder=json.dumps):
        return encoder(self.to_dict())
        # return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, data: Union[str, bytes, bytearray]):
        return cls.from_dict(json.loads(data))
