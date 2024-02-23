import sys

from utils.yaml_control import read_yanl


def generate_module_id():
    for i in range(1, 9999):
        module_id = "Module_ID" + "_" + str(i).zfill(2) + "_"
        yield module_id


def generate_interface_id():
    for i in range(1, 9999):
        interface_id = "Interface_ID" + "_" + str(i).zfill(2) + "_"
        yield interface_id


def generate_case_id():
    for i in range(1, 99999):
        case_id = "Case_ID" + "_" + str(i).zfill(2) + "_"
        yield case_id


module_id = generate_module_id()
interface_id = generate_interface_id()
case_id = generate_case_id()


def feature_info(yanl_path):
    allure_feature_info = next(module_id) + read_yanl(yanl_path)[0]["allure_common"]["allure_feature"]
    return allure_feature_info


def story_info(yanl_path):
    allure_story_info = next(interface_id) + read_yanl(yanl_path)[0]["allure_common"]["allure_story"]
    return allure_story_info


def title_info(yanl_path):
    allure_title_info = next(case_id) + read_yanl(yanl_path)[0]["allure_common"]["allure_title"]
    return allure_title_info


if __name__ == '__main__':
    # print(feature_info(
    #     r"D:\pytest-auto-api2-master\pytest-auto-api2-master\pythonProject\testcase\CrmLogin\CrmLogin.yaml"))
    # print(story_info(
    #     r"D:\pytest-auto-api2-master\pytest-auto-api2-master\pythonProject\testcase\CrmLogin\CrmLogin.yaml"))
    # print(title_info(
    #     r"D:\pytest-auto-api2-master\pytest-auto-api2-master\pythonProject\testcase\CrmLogin\CrmLogin.yaml"))
    print(sys.executable)