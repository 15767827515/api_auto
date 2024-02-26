import json
from json import JSONDecodeError

import allure
import pytest
import requests

from config.setting import ROOT_PATH
from utils.assert_control import AssertionMangement
from utils.extract_control import extract_data, replace_util, write_extract_yaml
from utils.generate_case_id import module_id, interface_id, case_id
from utils.read_config import ConfigParser
from utils.recordlog import logs
from utils.yaml_control import read_test_yaml


class RequestBase:

    def send_request(self, **kwargs):
        session = requests.session()
        result = None
        try:
            result = session.request(**kwargs)
            set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
            cookie = {}
            if set_cookie:
                cookie["cookie"] = set_cookie
                write_extract_yaml(cookie)
        except requests.exceptions.ConnectionError:
            logs.error("ConnectionError--连接异常")
            pytest.fail("接口请求异常，可能是request的连接数过多或请求速度过快导致程序报错！")
        except requests.exceptions.HTTPError:
            logs.error("HTTPError--http异常")
            pytest.fail(f"请求异常:{requests.exceptions.HTTPError}")
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail("请求异常，请检查系统或数据是否正常！")
        return result

    def run_main(self, name, url, case_name, header, method, cookies=None, file=None, **kwargs):
        try:
            logs.info('接口名称：{}'.format(name))
            logs.info('接口请求地址：{}'.format(url))
            logs.info(f'测试用例名称：{case_name}')
            logs.info(f'请求头：{header}')
            logs.info(f'cookies：{cookies}')
            req_params = json.dumps(kwargs, ensure_ascii=False)
            logs.info(f'请求参数：{list(eval(req_params).values())[0]}')
        except Exception as e:
            logs.info(e)
        result = self.send_request(url=url, headers=header, method=method, cookies=cookies, files=file,
                                   verify=False, **kwargs)
        return result

    def request_base(self, baseinfo: dict, testdata: dict):
        '''

        :param baseinfo:
        :param testdata:
        :return:
        '''
        try:
            feature_name = baseinfo["feature_name"]
            allure.dynamic.feature(feature_name)

            api_name = baseinfo["api_name"]
            allure.dynamic.story(next(interface_id) + api_name)
            allure.attach(api_name, f"接口测试的api名字是{api_name}", attachment_type=allure.attachment_type.TEXT)
            if baseinfo["url"].startswith("http"):
                url = replace_util(baseinfo["url"])
            else:
                url = ConfigParser.get_envi_api("host") + replace_util(baseinfo["url"])
                allure.attach(url, f"接口测试的url是{url}", attachment_type=allure.attachment_type.TEXT)

            method = baseinfo["method"]
            allure.attach(method, f"接口测试的请求方法是{method}", attachment_type=allure.attachment_type.TEXT)

            cookie = None
            if baseinfo.get("cookies") is not None:
                cookie = eval(replace_util(baseinfo['cookies']))
            allure.attach(json.dumps(cookie), f"接口测试的cookies信息是{json.dumps(cookie)}",
                          attachment_type=allure.attachment_type.TEXT)

            header = baseinfo["header"]
            if header is not None:
                header = replace_util(header)
            allure.attach(json.dumps(header), f"接口测试的header是{json.dumps(header)}",
                          attachment_type=allure.attachment_type.TEXT)

            # 提取测试用例名字
            case_name = replace_util(testdata.pop('case_name', None))
            allure.dynamic.title(next(case_id) + case_name)

            # 提取断言
            assertion = testdata.pop('assertion', None)

            # 处理变量提取
            extract = testdata.pop('extract', None)
            extract_list = testdata.pop('extract_list', None)

            # 处理文件上传
            file, files = testdata.pop('file', None), None
            if file is not None:
                for fk, fv in file.items():
                    files = {fk: open(fv, mode='rb')}
                    allure.attach(json.dumps(file), '导入文件')
            # allure.attach(json.dumps(file), f"接口测试的需要上传的文件路径是{json.dumps(file)}", attachment_type=allure.attachment_type.TEXT)

            params_type = ['data', 'json', 'params']
            # 处理请求传参
            for key, value in testdata.items():
                if key in params_type:
                    testdata[key] = replace_util(value)
                allure.attach(json.dumps(testdata),
                              f"接口测试的参数类型是{json.dumps(key)}，请求数据是{json.dumps(value)}",
                              attachment_type=allure.attachment_type.TEXT)

            result = self.run_main(name=api_name, url=url, case_name=case_name, header=header, method=method,
                                   cookies=None,
                                   file=files, **testdata)
            allure.attach(json.dumps(result.text), f"接口测试返回的结果是{result.text}",
                          attachment_type=allure.attachment_type.TEXT)
            allure.attach(json.dumps(assertion), f"接口测试的断言表达式是{json.dumps(assertion)}",
                          attachment_type=allure.attachment_type.TEXT)
            allure.attach(json.dumps(extract), f"接口测试需要提取的变量是{json.dumps(extract)}",
                          attachment_type=allure.attachment_type.TEXT)

            try:
                result_json = json.loads(result.text)
                if result:
                    logs.info(f'请求返回数据是：{result_json}')
                    # 提取关联变量
                    if extract is not None:
                        extract_data(extract, result_json)

                    # 调用断言方法
                    if assertion is not None:
                        AssertionMangement().assert_result(assertion, result_json)
            except JSONDecodeError as js:
                logs.info(f'请求返回数据是：{result.text}')
                logs.error('系统异常或接口未请求！')
                raise js
            except Exception as e:
                logs.error(e)
                raise e



        except Exception as e:
            logs.error(e)
            raise e


if __name__ == '__main__':
    baseinfo = {'api_name': '登录', 'url': '/prod-api/login', 'method': 'post', 'header': ''}
    testdata = {'case_name': '登录', 'json': {'username': 'admin',
                                              'password': 'jcqATMz+grB792HJWiTjz1icJkOck/wOgh0q2O2DfslWAmSl912+7H48D4w8y8w/71FcxNmrWXj09y3nvK3AKg=='}
                }
    #
    RequestBase().request_base(baseinfo, testdata)
