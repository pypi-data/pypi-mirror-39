import uuid
import decimal
from abc import ABC, abstractmethod


class Field(ABC):
    @classmethod
    @abstractmethod
    def _serialize(cls, value):
        pass

    @classmethod
    @abstractmethod
    def _deserialize(cls, value):
        pass


class UUID(Field):

    __slots__ = ()

    @classmethod
    def _serialize(cls, value):
        return str(value) if value is not None else None

    @classmethod
    def _deserialize(cls, value):
        if isinstance(value, uuid.UUID):
            return value
        try:
            if isinstance(value, bytes) and len(value) == 16:
                return uuid.UUID(bytes=value)
            else:
                return uuid.UUID(value)
        except (ValueError, AttributeError, TypeError):
            raise ValueError("Not a valid UUID")


class Decimal(Field):
    def __init__(self, places=None, rounding=None):
        if places is not None:
            self.places = decimal.Decimal((0, (1,), -places))
        else:
            self.places = None
        self.rounding = rounding

    @classmethod
    def _serialize(self, value):
        if self.places:
            return str(value.quantize(self.places), self.rounding)
        else:
            return str(value)

    @classmethod
    def _deserialize(cls, value):
        pass
