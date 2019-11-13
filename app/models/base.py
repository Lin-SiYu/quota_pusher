from lib.db.db_utils import MysqlPool
from peewee import Model


class BaseModel(Model):
    # 默认字段
    ...

    class Meta:
        database = MysqlPool().get_conn()
        legacy_table_names = False
