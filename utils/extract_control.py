import json

import jsonpath
import yaml
from config.setting import extract_yanl_path
from utils.debugtalk import DebugTalk
from utils.recordlog import logs
import re


def replace_util(data):
    '''
    """yaml数据替换解析"""
    :param data:
    :return:
    '''
    str_data = data
    if not isinstance(data, str):
        str_data = json.dumps(data)
    for i in range(str_data.count("${")):
        if '${' in str_data and '}' in str_data:
            logs.info('替换后的数据：{}'.format(str_data))
            start_index = str_data.index('$')
            end_index = str_data.index("}", start_index)
            # 提取包含函数名和参数的字符串
            full_expression = str_data[start_index:end_index + 1]
            # 取出yaml文件的函数名
            func_name = full_expression[2:full_expression.index("(")]

            # 提取函数参数
            func_params = full_expression[full_expression.index("(") + 1:full_expression.index(")")]

            # 使用 getattr 调用 DebugTalk 类中的方法，传递函数参数
            extract_data = getattr(DebugTalk(), func_name)(*func_params.split(",") if func_params else "")
            if extract_data and isinstance(extract_data, list):
                extract_data=(",").join(i for i in extract_data)
            # 字符串replace需要重新赋值给str_data
            str_data=str_data.replace(full_expression,str(extract_data))
            logs.info('替换后的数据：{}'.format(str_data))
    if data and isinstance(data, dict):
        data = json.loads(str_data)
    else:
        data = str_data
    return data


def extract_data(testdata_extract_list: list, response):
    '''
    提取接口的返回值，支持正则表达式和json提取器
    :param testdata_extract_expression:testcase文件yaml中的extract值
    :param response:接口的实际返回值
    :return:
    '''
    try:
        pattern_lst = ['(.*?)', '(.+?)', r'(\d)', r'(\d*)']
        for testdata_extract in testdata_extract_list:
            for key, value in testdata_extract.items():
                # 处理正则表达式提取
                for pat in pattern_lst:
                    if pat in value:
                        ext_lst = re.search(str(value), str(response))
                        if ext_lst is None:
                            logs.error("响应结果中没有匹配到值，请检查正则表达式是否正确")
                        else:
                            if pat in [r'(\d+)', r'(\d*)']:
                                extract_data = {key: int(ext_lst)}
                                logs.info('从接口提取的返回值：{}'.format(extract_data))
                            else:
                                extract_data = {key: ext_lst.group(1)}
                                logs.info('从接口提取的返回值：{}'.format(extract_data))
                            write_extract_yaml(extract_data)
                # 处理json提取参数
                if '$' in value:
                    ext_json = jsonpath.jsonpath(response, value)[0]
                    if ext_json:
                        extarct_data = {key: ext_json}
                        logs.info('从接口提取的返回值：{}'.format(extarct_data))
                    else:
                        extarct_data = {key: '未提取到数据，请检查接口返回值是否为空！'}
                        logs.info('从接口提取的返回值：{}'.format(extarct_data))
                    write_extract_yaml(extarct_data)
    except Exception as e:
        logs.error(e)


def write_extract_yaml(data, extract_yanl_path=extract_yanl_path):
    '''
    将提取到的变量写入extract_yanl_path文件中
    :param data: 要写入的数据
    :param extract_yanl_path: 保存提取变量的文件路径
    :return:
    '''
    try:
        if isinstance(data, dict):
            with open(extract_yanl_path, 'a', encoding="utf-8") as f:
                data = yaml.dump(data, allow_unicode=True)
                f.write(data)
        else:
            print('写入到[extract_yanl_path.yaml]的数据必须是字典类型格式！')
    except Exception as e:
        logs.info(e)

def clean_extract_yaml(filepath: object = extract_yanl_path) -> object:
    '''
    清除extract.yaml文件的数据
    :param filepath: extract.yaml的路径，默认为
    :return:
    '''
    try:
        with open(filepath,"w") as f:
            f.truncate()
    except Exception as e:
        logs.error(e)


if __name__ == '__main__':
    exp = [{"token": "'token': '(.*?)'"}]
    response = r"{'orgId': '4140913758110176843','token': '啊啊啊aD2EFABD3DC2d2Aa361c87bdcaAba啊啊啊'}"
    # print(extract_data(exp, response))

    # exp = {"token": "$.token"}
    # response = {"token": "aD2EFABD3DC2d2Aa361c87bdcaAba"}
    # print(extract_data(exp, response))
    # print(replace_util("user_name: ${get_extract_var(userId)}"))
    # clean_extract_yaml()
    # exp = "{'createTime': '(.*?)'}"
    # response ="{'code': 200, 'msg': '上传成功', 'data': [{'id': '3cce9868b99e433ba8d01f2960eff032', 'fileName': 'Test_20240222135346A052', 'createTime': '2024-02-22 13:53:46', 'filePath': 'E:\\ycansoft-crm\\uploadPath\\contractAttachment\\2024\\02\\22\\Test_20240222135346A052.xls', 'fileSize': 19968, 'extension': 'xls', 'status': '0', 'remark': None, 'contractId': '8b2e1d7733a340a4ab6b367809bf64d3', 'fileUrl': '/profile/contractAttachment/2024/02/22/Test_20240222135346A052.xls'}], 'error': False, 'success': True}"
    # res=re.search(str(exp),str(response))
    # print(res)
    data={'Authorization': '${get_authorization()}'}
    replace_util(data)
