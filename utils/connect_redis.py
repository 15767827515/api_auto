import redis

from utils.read_config import ConfigParser
from utils.recordlog import logs


class ConnnectRedis:

    def __init__(self):
        self.connect_info = {
            "host": ConfigParser.get_redis_options("host"),
            "port": ConfigParser.get_redis_options("port"),
            "username": ConfigParser.get_redis_options("username"),
            "password": ConfigParser.get_redis_options("password"),
            "db": ConfigParser.get_redis_options("db"),
            "decode_responses" : True
        }

        self.connection_pool=redis.ConnectionPool(**self.connect_info)
        self.con=redis.Redis(connection_pool=self.connection_pool)


    def get(self,key):
        '''
        根据key获取Redis的值
        :param key:
        :return:
        '''
        try:
            result=self.con.get(key)
            if isinstance(result,bytes):
                return result.decode("utf-8")
            return result
        except Exception as e:
            logs.error(f'Redis Error：{e}')

    def set(self,key,value,ex=None):
        try:
            self.con.set(key,value,ex=ex)
        except Exception as e:
            logs.error(f'Redis Error：{e}')


if __name__ == '__main__':
    print(ConnnectRedis().get("identifys"))
    ConnnectRedis().set("identifys",2222)
    print(ConnnectRedis().get("identifys"))
