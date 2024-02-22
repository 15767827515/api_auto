import pymssql
import pymysql

from utils.read_config import ConfigParser
from utils.recordlog import logs


class SqlserverConnect:

    def __init__(self):
        self.connect_info = {
            "host": ConfigParser.get_serversql_options("host"),
            "port": int(ConfigParser.get_serversql_options("port")),
            "user": ConfigParser.get_serversql_options("user"),
            "password": ConfigParser.get_serversql_options("password"),
            "database": ConfigParser.get_serversql_options("database"),
            "charset": "UTF-8"
        }

        self.connect = pymssql.connect(**self.connect_info)
        # cursor=pymysql.cursors.DictCursor 将结果返回字典类型
        self.cursor = self.connect.cursor(as_dict=True)

    def query(self, sql, query_type="one"):
        '''
        查询数据库
        :param sql: 需要查询的sql语句
        :param query_type:查询类型，默认查询单条数据，传all查询全部数据
        :return:
        '''
        try:
            self.cursor.execute(sql)
            result = None
            if query_type.upper() == 'ONE':
                result = self.cursor.fetchone()
            elif query_type.upper() == 'ALL':
                result = self.cursor.fetchall()
            return result
        except AttributeError as error:
            logs.error(f"数据库查询失败，失败原因：{error}")

    def execute(self, sql):
        '''
        执行sql的增删改的操作
        :param sql: 增删改的sql语句
        :return:
        '''
        try:
            result = self.cursor.execute(sql)
            self.connect.commit()
            return result
        except Exception as e:
            self.connect.rollback()
            logs.error(f"数据库操作失败，失败原因：{e}")

    def __del__(self):
        try:
            self.connect.close()
            self.cursor.close()
        except AttributeError as error:
            logs.error(error)


class MysqlConnect:
    def __init__(self):
        self.connect_info = {
            "host": ConfigParser.get_mysql_options("host"),
            "port": int(ConfigParser.get_mysql_options("port")),
            "user": ConfigParser.get_mysql_options("user"),
            "password": ConfigParser.get_mysql_options("password"),
            "database": ConfigParser.get_mysql_options("database"),
        }
        self.connect = pymysql.connect(**self.connect_info)
        # cursor=pymysql.cursors.DictCursor 将结果返回字典类型
        self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)

    def query(self, sql, query_type="one"):
        try:
            self.cursor.execute(sql)
            result = None
            if query_type.upper() == 'ONE':
                result = self.cursor.fetchone()
            elif query_type.upper() == 'ALL':
                result = self.cursor.fetchall()
            return result
        except AttributeError as error:
            logs.error(f"数据库查询失败，失败原因：{error}")

    def execute(self, sql):
        try:
            result = self.cursor.execute(sql)
            self.connect.commit()
            return result
        except Exception as e:
            self.connect.rollback()
            logs.error(f"数据库操作失败，失败原因：{e}")

    def __del__(self):
        try:
            self.connect.close()
            self.cursor.close()
        except AttributeError as error:
            logs.error(error)


if __name__ == '__main__':
    sql = "select * from 销项发票 where 发票GUID='3d980d9f-6cb4-407c-89d1-86030be8fe98'"
    print(SqlserverConnect().query(sql, "one"))
    sql2= "update  销项发票 set 开票机号=200 where 发票GUID='3d980d9f-6cb4-407c-89d1-86030be8fe98'"
    print(SqlserverConnect().execute(sql2))
    print(SqlserverConnect().query(sql, "one"))

    sql3="select 开票机号 from 销项发票 where 发票GUID='3d980d9f-6cb4-407c-89d1-86030be8fe98'"

    print(SqlserverConnect().query(sql3))
