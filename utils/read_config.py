import configparser

from config.setting import config_path


class ConfigControl:

    # 初始化configini文件路径和初始化ConfigParser对象
    def __init__(self):
        self.filepath = config_path
        self.config = configparser.ConfigParser()
        self.config.read(self.filepath)

    # 获取所有的sections，已列表形式返回
    def get_sections(self):
        result=self.config.sections()
        return result

    #获取对应section下的所有options
    def get_options(self,section):
        '''

        :param section: 具体的分组名称
        :return:
        '''
        result=self.config.options(section)
        return result

    # 获取对应section下的具体的options
    def get_specific_options(self,section,name):
        '''

        :param section: 具体的分组名称
        :param name: 具体的分组下元素的key值
        :return:
        '''
        result=self.config.get(section,name)
        return result

    def get_serversql_options(self,name):
        '''
        读取配置文件中sqlserver的信息
        :param section: 具体的分组名称
        :param name: 具体的分组下元素的key值
        :return:
        '''
        result=self.get_specific_options(section="SQLSERVER",name=name)
        return result

    def get_mysql_options(self,name):
        '''
        读取配置文件中mysql的信息
        :param section: 具体的分组名称
        :param name: 具体的分组下元素的key值
        :return:
        '''
        result=self.get_specific_options(section="MYSQL",name=name)
        return result

    def get_redis_options(self,name):
        '''
        读取配置文件中REDIS的信息
        :param section: 具体的分组名称
        :param name: 具体的分组下元素的key值
        :return:
        '''
        result=self.get_specific_options(section="REDIS",name=name)
        return result

    def get_envi_api(self,name):
        '''
        读取配置文件中环境api的信息
        :param name:
        :return:
        '''
        result = self.get_specific_options(section="envi_api", name=name)
        return result

ConfigParser=ConfigControl()

if __name__ == '__main__':
    # print(ConfigControl().get_sections())
    # print(ConfigControl().get_options("MYSQL"))
    # print(ConfigControl().get_specific_options("MYSQL","host"))
    print(ConfigControl().get_serversql_options(name="host"))