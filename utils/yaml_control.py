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
    row_data = read_yanl(yanl_path)[0]
    testcase_list = []
    if row_data:
        baseinfo = row_data["baseInfo"]
        for testdata in row_data["testCase"]:
            testcase_list.append((baseinfo, testdata))
    return testcase_list


if __name__ == '__main__':

    print(read_yanl(r"D:\pytest-auto-api2-master\pytest-auto-api2-master\pythonProject\testcase\CrmLogin\CrmLogin.yaml")[0]["allure_common"])
