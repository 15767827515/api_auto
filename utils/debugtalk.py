import base64
from faker import Faker
import hashlib
import os
import random
import string
import time
from datetime import datetime

import rsa
import yaml
# from crypto.Cipher import PKCS1_v1_5
# from crypto.PublicKey import RSA

from config.setting import extract_yanl_path, ROOT_PATH, public_key_path

from utils.read_config import ConfigControl, ConfigParser
from utils.recordlog import logs

import base64


class DebugTalk:
    def __init__(self):
        self.zh_fk = Faker(locale="zh_CN")

    def get_authorization(self, extract_yaml_file=extract_yanl_path):
        '''
        获取Bearer token的authorization
        :param extract_yaml_file:
        :return:
        '''
        try:
            with open(extract_yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                authorization = "Bearer" + " " + data["token"]
            return authorization

        except Exception as e:
            logs.info(e)

    def get_extract_var(self, var_key, index=None, extract_yaml_file=extract_yanl_path):
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
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return data

    def md5_encryption(self, data):
        md5_data = hashlib.md5(str(data).encode()).hexdigest()
        return md5_data

    def base64_encryption(self, data):
        base64_data = base64.b64encode(str(data).encode())
        return base64_data

    def sha1_encryption(self, data):
        sha1_data = hashlib.sha1(str(data).encode()).hexdigest()
        return sha1_data

    def sha256_encryption(self, data):
        sha256_data = hashlib.sha256(str(data).encode()).hexdigest()
        return sha256_data

    def RSA_encryption(self, data: str, public_path=public_key_path):
        try:
            with open(public_path) as f:
                jk = f.read()
        except Exception as e:
            logs.error(e)
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(jk.encode())
        data_byts = rsa.encrypt(data.encode(), pubkey)
        rsa_data = base64.b64encode(data_byts).decode()
        return rsa_data

    def get_timestamp(self):

        current_utc_time = time.gmtime()
        timestamp_seconds = time.mktime(current_utc_time)
        # 将秒级时间戳转换为毫秒级时间戳
        timestamp = str(int(timestamp_seconds * 1000))

        return timestamp

    def get_sign(self, appid=ConfigParser.get_sign_options("appid"),
                 publicKey=ConfigParser.get_sign_options("publicKey")):
        timestamp = self.get_timestamp()
        input_string = f"{appid}{publicKey}{timestamp}"
        md5_hash = hashlib.md5(input_string.encode('utf-8')).hexdigest()
        return md5_hash

    def generate_taxno(self, length=20):
        # 将所有字母和数字拼接成一个字符串characters
        characters = string.ascii_uppercase + string.digits + string.ascii_lowercase
        random_taxno = ''
        for i in range(length):
            random_taxno = random_taxno + random.choice(characters)
        return random_taxno

    def generate_companyname(self, length=10):
        # 将所有字母和数字拼接成一个字符串characters
        characters = "投保单尾数选其中一个它就会合并一起付款了付完款把付款界面截图下来然后发我一个给您安排返现然后那个礼品的话你把地址发给我"
        random_companyname = ''
        for i in range(length):
            random_companyname = random_companyname + random.choice(characters)
        random_companyname += "有限公司"
        return random_companyname

    def generate_randon_int(cls, *args):
        """
               :return: 随机数
        """
        if not args:
            return random.randint(0, 9999)
        else:
            min_num = min(*args)
            max_num = max(*args)
            return random.randint(min_num, max_num)

    def generate_randon_company_name(self):
        '''
        随机生成公司名字
        :return:
        '''
        return "test_" + self.zh_fk.company()

    def generate_randon_phone_number(self):
        '''
        随机生成手机号码
        :return:
        '''
        return self.zh_fk.phone_number()

    def generate_randon_name(self):
        '''
        随机生成人名
        :return:
        '''
        return self.zh_fk.name()

    def generate_randon_id(self):
        '''
        随机生成身份证号码
        :return:
        '''
        return self.zh_fk.ssn()

    def generate_randon_email(self):
        '''
        随机生成邮箱
        :return:
        '''
        return self.zh_fk.email()


if __name__ == '__main__':
    # print(DebugTalk().get_extract_var("orgId", 0))
    # data = "V{Fc~39m"

    # print(random.choice(['A5DBa8CdFabEdfC06FDbE5AC4aF87', 'A5DBa8CdFabEdfC06FDbE5AC4aF872', 'A5DBa8CdFabEdfC06FDbE5AC4aF87']))
    # print(DebugTalk().get_now_date())
    # print(DebugTalk().md5_encryption(data))
    # print(DebugTalk().base64_encryption(data))
    # print(DebugTalk().sha1_encryption(data))
    # print(DebugTalk().sha256_encryption(data))
    # print(DebugTalk().RSA_encryption(data))
    # print(DebugTalk().get_timestamp())
    # print(DebugTalk().get_sign())
    # from utils.extract_control import replace_util
    # url="http://192.168.2.118:84/HttpYnInvOcrCheck.jsp?appid=002a005801a34d818ce14977e6c592c9&timestamp=${get_timestamp()}&ischeck=1&systemname=ctg&usertag=ctg&billno=ctg&sign=${get_sign(\"102a005801a34d818ce14977e6c592c9\",\"2a3a75caf3a5f2efac2106237bb040fb\")}"
    # data=replace_util(url)
    # print(data)
    print(DebugTalk().generate_taxno())
    print(DebugTalk().generate_companyname())
