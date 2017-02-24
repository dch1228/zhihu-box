DEBUG = False

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'zhihu_zhuanlan'

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

ZHIHU_USER = ''
ZHIHU_PASSWORD = ''

try:
    from local_setting import *
except ImportError:
    pass
