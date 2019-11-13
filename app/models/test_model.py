import peewee

from .base import BaseModel


class TestModel(BaseModel):
    text = peewee.CharField()
