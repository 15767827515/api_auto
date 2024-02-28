import redis

# from rediscluster import RedisCluster



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
            "decode_responses": True
        }
        # 获取redis集群的节点
        startup_nodes_str=ConfigParser.get_redis_options("startup_nodes")
        self.nodes_list = []
        try:
            # 判断redis下的startup_nodes_str是否为空，来执行集群连接或者是单服务连接
            if startup_nodes_str:
                startup_nodes_list=startup_nodes_str.split(";")
                host, port=None,None
                for node in startup_nodes_list:
                    host,port=node.split(":")
                    self.nodes_list.append({"host":host,"port":port})
                self.con=RedisCluster(startup_nodes=self.nodes_list)
            elif self.connect_info['host'] and self.connect_info['port']:
                self.con = redis.StrictRedis(**self.connect_info)
        except Exception as e:
            logs.error(e)



    def get(self, key):
        '''
        根据key获取Redis的值
        :param key:
        :return:
        '''
        try:
            result = self.con.get(key)
            if isinstance(result, bytes):
                return result.decode("utf-8")
            return result
        except Exception as e:
            logs.error(f'Redis Error：{e}')

    def set(self, key, value, ex=None):
        '''
        根据key设置对应的redis value
        :param key:
        :param value:
        :param ex:
        :return:
        '''
        try:
            self.con.set(key, value, ex=ex)
        except Exception as e:
            logs.error(f'Redis Error：{e}')


if __name__ == '__main__':
    print(ConnnectRedis().get("identifys"))
    ConnnectRedis().set("identifys", 2222)
    print(ConnnectRedis().get("identifys"))




