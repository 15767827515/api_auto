import yaml

from utils.recordlog import logs


def read_yanl(yanl_path):
    '''
    :param yanl_path:
    :return:
    '''
    try:
        with open(yanl_path, 'r', encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data
    except Exception as e:
        logs.error(e)



def read_test_yaml(yanl_path):
    '''
    读取测试用例yaml文件
    :param yanl_path:
    :return:
    '''
    row_data = read_yanl(yanl_path)
    testcase_list = []
    if row_data:
        for interface_info in row_data:
            baseinfo = interface_info["baseInfo"]
            for testdata in interface_info["testCase"]:
                testcase_list.append((baseinfo, testdata))
    return testcase_list


if __name__ == '__main__':
    print(read_test_yaml(r"D:\pytest-auto-api2-master\pytest-auto-api2-master\pythonProject\testcase\SMOKE\smoke.yaml"))
