import peewee

from .base import BaseModel


class User(BaseModel):
    id = peewee.IntegerField()
    name = peewee.CharField()
    age = peewee.CharField()
