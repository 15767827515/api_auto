import json

import pytest
import requests

from config.setting import ROOT_PATH
from utils.extract_control import extract_data, replace_util
from utils.read_config import ConfigParser
from utils.recordlog import logs
from utils.yaml_control import read_test_yaml


class RequestBase:

    def send_request(self, **kwargs):
        session = requests.session()
        result = session.request(**kwargs)
        return result

    def run_main(self, name, url, case_name, header, method, cookies=None, file=None, **kwargs):
        try:
            logs.info('接口名称：{}'.format(name))
            logs.info('接口请求地址：{}'.format(url))
            logs.info(f'测试用例名称：{case_name}')
            logs.info(f'请求头：{header}')
            logs.info(f'cookies：{cookies}')
            req_params = json.dumps(kwargs, ensure_ascii=False)
            logs.info(f'请求参数：{kwargs}')
            result = self.send_request(url=url, headers=header, method=method, cookies=cookies, files=file,
                                       verify=False, **kwargs)
            return result
        except Exception as e:
            logs.info(e)

    def request_base(self, baseinfo, testdata):
        '''

        :param baseinfo:
        :param testdata:
        :return:
        '''
        try:
            api_name = baseinfo["api_name"]
            url = ConfigParser.get_envi_api("host") + baseinfo["url"]
            method = baseinfo["method"]
            header = baseinfo["header"]
            params_type = ['data', 'json', 'params']
            # 提取测试用例名字
            case_name = replace_util(testdata.pop('case_name', None))

            # 提取断言
            assertion = testdata.pop('assertion', None)

            # 处理变量提取
            extract = testdata.pop('extract', None)
            extract_list=testdata.pop('extract_list', None)

            # 处理文件上传
            file, files = replace_util(testdata.pop('file', None)), None
            if file is not None:
                for fk, fv in file.items():
                    files = {fk: open(fv, mode='rb')}


            # 处理请求传参
            for key, value in testdata.items():
                if key in params_type:
                    testdata[key] = replace_util(value)

            result = self.run_main(name=api_name, url=url, case_name=case_name, header=header, method=method,
                                   cookies=None,
                                   file=files, **testdata)
            try:
                if result:
                    result = result.json()
                    logs.info(f'请求返回数据是：{result}')
            except Exception as e:
                result = result.text
                logs.error(f'请求返回数据不是json，无法转换，接口返回原始数据是：{result}!/n 异常信息是:{e}')
            print(extract)
            if extract is not None:
                extract_data(extract, result)
        except Exception as e:
            logs.error(e)

    def md5_encry(self):
        pass


if __name__ == '__main__':
    baseinfo = {'api_name': '上传文件', 'url': '/prod-api/crmContract/contract/attachment/upload', 'method': 'post',
                'header': {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjE2OWVmODhiLTI3ODUtNGZjZi05NjY2LTVhMjUyMmZlZjVmYSJ9.nlG6wiPp8eBpn7erSQV5-QeR2dcCkfYSfb_sXtUgrSFGcezEYyYQXIgf7Am_nN92yBUG-aPYMvs5Tf65y-UT_w'}}
    testdata = {'case_name': '上传excel文件', 'data': {'contractId': '8b2e1d7733a340a4ab6b367809bf64d3'},
                'file': {'files': '../data/Test.xls'}}
    #
    RequestBase().request_base(baseinfo, testdata)

