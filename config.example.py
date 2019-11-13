SITE_NAME = '令牌II'
COOKIE_SECRET = 'THIS_IS_COOKIE_SECRET'
PORT = 8080
DEBUG = False

MAIL_LIST = ['notify_robot@163.com']
SEND_MAIL = False

SHUTDOWN_MAX_WAIT_TIME = 1 * 1
INFO_LOG_PATH = "./logs/info.log"
DEBUG_LOG_PATH = "./logs/debug.log"
ERROR_LOG_PATH = "./logs/error.log"
ACC_LOG_PATH = "./logs/access.log"
LOG_BACKUP = 7
LOG_ROTATE_DAY = 7

MONGO_URI = 'mongodb://root:password@localhost:27017/test'
MONGO_DB = 'test'

REDIS_URL = 'redis://localhost:6379/'
REDIS_DB = 0

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PWD = 'root'
DB_MAX = 10
DB_NAME = 'test'

MQ_HOST = '127.0.0.1'
MQ_PORT = 5672
MQ_USER = 'test'
MQ_PWD = '123'
MQ_VHOST = '/'

HEARTBEAT_INTERVAL = 30
HEARTBEAT_BROADCAST = 30

EXCHANGES_DICT = {
    'fanout': ['Heartbeat', 'Example'],
    'topic': ['MarketPair'],
    'direct': []
}

MIDDLEWARE_LIST = [
    'lib.middleware.ping_middle.PingMiddleware',
]
# 用于给 ws 连接用户发送 ping，确认连接,若不配置，则不发送
BEAT_PING_INTERVAL = 30
