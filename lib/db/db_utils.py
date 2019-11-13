from peewee_async import Manager, PooledMySQLDatabase
from tornado.options import options


class MysqlPool:

    @classmethod
    def from_config(cls):
        data = options.as_dict().copy()
        return dict(
            host=data.pop('DB_HOST'),
            port=data.pop('DB_PORT', 3306),
            user=data.pop('DB_USER'),
            password=data.pop('DB_PWD'),
            max_connections=data.pop('DB_MAX', 10),
            database=data.pop('DB_NAME', 10),
        )

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            kwargs = cls.from_config()
            cls.conn = PooledMySQLDatabase(**kwargs, charset='utf8mb4')
            cls.manager = Manager(cls.conn)
            cls._instance = super(MysqlPool, cls).__new__(cls)
        return cls._instance

    def get_conn(self):
        return self.conn

    def get_manager(self):
        return self.manager
