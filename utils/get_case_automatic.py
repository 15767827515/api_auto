import os
import textwrap

from config.setting import testdata_path, real_time_update_test_cases
from config.setting import testcase_path
from utils.recordlog import logs
from utils.yaml_control import read_yanl


class TestCaseAutomaticGeneration:

    def get_all_testdata_path(self, testdata_path=testdata_path):
        '''
        获取测试用例文件下的所有yaml路径
        :param testdata_path:  默认读取配置文件的测试用例路径
        :return:
        '''
        file_path_list = []
        for root, dirs, files in os.walk(testdata_path):  # 遍历测试用例文件夹
            for file in files:  # 遍历所有文件
                file_path = os.path.join(root, file)  # 将路径和文件拼接成测试用例的完整路径
                if file_path:
                    file_path_list.append(file_path)
        return file_path_list

    def get_case_file_name(self, file_path: str):
        '''
        获取yaml测试文件的文件名
        :param file_path: yaml测试文件的完整路径
        :return:
        '''
        case_file_name = None
        case_with_suffix_name = file_path.split(os.sep)[-1]
        if case_with_suffix_name.endswith("yaml"):
            case_file_name = case_with_suffix_name[:-5]
        elif case_with_suffix_name.endswith("yal"):
            case_file_name = case_with_suffix_name[:-4]
        return case_file_name

    def get_case_dir_name(self, file_path: str):
        '''
        获取yaml测试文件的上级文件夹名字
        :param file_path: yaml测试文件的完整路径
        :return:
        '''

        case_dir_name = None
        case_dir_name = file_path.split(os.sep)[-2]
        return case_dir_name

    def mk_case_dir(self, file_path):
        '''
        在testcase路径下创建  与yaml用例上级文件夹同名  的文件夹
        :param file_path:
        :return:
        '''
        # 获取yaml测试文件的上级文件夹名字
        case_dir_name = self.get_case_dir_name(file_path)
        # 取yaml测试文件的上级文件夹与testcase路径拼成新文件夹的路径
        case_dir_path = os.path.join(testcase_path, case_dir_name)
        try:
            if os.path.exists(testcase_path):
                os.mkdir(case_dir_path)

        except Exception as e:
            logs.error(f"{case_dir_path}这个文件夹已存在，无需重复创建")

        finally:
            return case_dir_path

    def generate_case_full_path(self, file_path):
        '''
        根据yaml测试文件的文件名，生成测试脚本文件的全路径
        :param file_path:
        :return:
        '''
        # 获取yaml测试文件的上级文件夹名字
        case_dir_name = self.get_case_dir_name(file_path)
        # 将testcase路径与上级文件夹名字拼接得到测试脚本的上级文件夹的路径
        case_dir_path = os.path.join(testcase_path, case_dir_name)
        ## 拼接得到测试脚本的完整路径
        case_name = case_dir_path + os.sep + "test_" + self.get_case_file_name(file_path) + ".py"
        return case_name

    def generate_case_class_name(self, file_path):

        split_name_list = self.get_case_file_name(file_path).split("_")
        capitalize_split_name_list = []
        case_class_name = None
        for i in split_name_list:
            capitalize_split_name_list.append(i.capitalize())
            case_class_name = "Test" + "".join(capitalize_split_name_list)
        return case_class_name

    def generate_case_function_name(self, file_path):

        case_function_name = "test_" + self.get_case_file_name(file_path)
        return case_function_name

    def write_testcase_file(self, testcase_path, testdata_yaml_path, class_name, function_name):

        page = f'''
import allure
import pytest
from config.setting import ROOT_PATH
from utils.request_control import RequestBase
from utils.yaml_control import read_test_yaml

class {class_name}:

    @pytest.mark.parametrize(('baseinfo,testdata'),
                     read_test_yaml(r"{testdata_yaml_path}"))
    def {function_name}(self,baseinfo,testdata):
        RequestBase().request_base(baseinfo,testdata)

'''
        indented_page = textwrap.indent(page, '')
        if real_time_update_test_cases:
            with open(testcase_path, 'w', encoding='utf-8') as file:
                file.write(indented_page)
        elif real_time_update_test_cases is False:
            if not os.path.exists(testcase_path):
                with open(testcase_path, 'w', encoding='utf-8') as file:
                    file.write(indented_page)

    def get_case_automatic(self) -> None:
        """自动生成 测试代码"""
        file_path_list = self.get_all_testdata_path()
        for file_path in file_path_list:
            # 判断代理拦截的yaml文件，不生成test_case代码
            if 'proxy_data.yaml' not in file_path:
                # 判断用例需要的文件夹路径是否存在，不存在则创建
                self.mk_case_dir(file_path)
                yaml_case_process = read_yanl(file_path)
                self.write_testcase_file(
                    testcase_path=self.generate_case_full_path(file_path),
                    testdata_yaml_path=file_path,
                    class_name=self.generate_case_class_name(file_path),
                    function_name=self.generate_case_function_name(file_path))


if __name__ == '__main__':
    TT = TestCaseAutomaticGeneration()
    file_path = r'D:\pytest-auto-api2-master\pytest-auto-api2-master\pythonProject\testdata\Smoking_Process\smoking _process.yaml'
    print(TT.get_case_file_name(file_path))
    print(TT.generate_case_class_name(file_path))
    print(TT.get_case_automatic())

1