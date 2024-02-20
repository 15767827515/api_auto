import json

import requests

from utils.extract_control import extract_data, repleace_util
from utils.recordlog import logs


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
            print(e)

    def request_base(self, baseinfo, testdata):
        '''

        :param baseinfo:
        :param testdata:
        :return:
        '''
        api_name = baseinfo["api_name"]
        url = r"http://127.0.0.1:8787" + baseinfo["url"]
        method = baseinfo["method"]
        header = baseinfo["header"]
        extract=None
        if "case_name" in testdata.keys():
            case_name = repleace_util(testdata.pop('case_name'))
        if "assertion" in testdata.keys():
            assertion = testdata.pop('assertion')
        if "extract" in testdata.keys():
            extract = repleace_util(testdata.pop('extract'))

        for key, value in testdata.items():
            testdata[key] = repleace_util(value)

        result = self.run_main(name=api_name, url=url, case_name=case_name, header=header, method=method, cookies=None,
                               file=None, **testdata).json()

        if extract:
            extract_data(extract, result)





    def md5_encry(self):
        pass


if __name__ == '__main__':
    baseinfo = {'api_name': '用户登录', 'url': '/dar/user/login', 'method': 'post',
                'header': {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}}
    testdata = {'case_name': '用户名和密码正确登录验证', 'data': {'user_name': 'test01', 'passwd': 'admin123'},
                'assertion': [{'contains': {'msg': '登录成功'}}],
                'extract': {'token': '$.token', 'userId': '$.userId'}}

    print(RequestBase().request_base(baseinfo, testdata))
