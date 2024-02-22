import datetime
import random

import yaml

from config.setting import extract_yanl_path
from utils.recordlog import logs

class DebugTalk:


    def get_authorization(self,extract_yaml_file=extract_yanl_path):
        try:
            with open(extract_yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                authorization="Bearer"+" "+data["token"]
            return authorization

        except Exception as e:
            logs.info(e)

    def get_extract_var(self,var_key, index=None, extract_yaml_file=extract_yanl_path):
        '''
        获取extract.yaml数据
        :param var_key: extract.yaml文件中的key值
        :param index: 根据索引取值，int类型，0：随机读取；负数：返回字符串形式；正数：根据index-1去索引列表
        :param extract_yaml_file:
        :return:
        '''
        try:
            with open(extract_yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            get_extract_var = None
            if index is None:
                get_extract_var = data[var_key]

            if index is not None:
                if isinstance(index, int):
                    if isinstance(data[var_key], list):

                        if index == 0:
                            get_extract_var = random.choice(data[var_key])

                        if index < 0:
                            get_extract_var = str(data[var_key])
                        if index > 0:
                            if len(data[var_key]) > (index - 1):
                                get_extract_var = data[var_key][index - 1]

                            else:
                                print("传入索引大于变量列表的长度")
                    else:
                        print("该变量值只有一个，不需要指定索引")
                else:
                    print("传入的索引值不为int类型")
            return get_extract_var

        except Exception as e:
            logs.info(e)

    def get_now_date(self):
        """
        获取当前日期的标准格式
        :return:
        """
        data=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return data

if __name__ == '__main__':
    # print(DebugTalk().get_extract_var("orgId", 0))

    # print(random.choice(['A5DBa8CdFabEdfC06FDbE5AC4aF87', 'A5DBa8CdFabEdfC06FDbE5AC4aF872', 'A5DBa8CdFabEdfC06FDbE5AC4aF87']))
    print(DebugTalk().get_now_date())