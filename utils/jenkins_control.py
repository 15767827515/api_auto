import jenkins

from utils.read_config import ConfigParser
import re

class JenkinsManege:

    def __init__(self):
        """
        初始化连接jenkins的信息
        """
        self.__conf = {
            "url": ConfigParser.get_jenkins("url"),
            "username": ConfigParser.get_jenkins("username"),
            "password": ConfigParser.get_jenkins("password")
        }
        self.job_name = ConfigParser.get_jenkins("job_name")
        self.__server = jenkins.Jenkins(**self.__conf)

    def get_job_number(self):
        '''
         读取jenkins job构建号
        :return:
        '''
        build_number = self.__server.get_job_info(self.job_name).get('lastBuild').get('number')
        return build_number

    def get_job_description(self):
        """返回job描述信息"""
        description = self.__server.get_job_info(self.job_name).get('description')
        url = self.__server.get_job_info(self.job_name).get('url')
        return description, url

    def get_build_job_status(self):
        """读取构建完成的状态"""
        job_status = self.__server.get_build_info(self.job_name, self.get_job_number()).get('result')
        return job_status

    def get_console_log(self):
        """获取控制台日志"""
        console_log = self.__server.get_build_console_output(self.job_name, self.get_job_number())
        return console_log

    def get_build_report(self):
        """返回第n次构建的测试报告"""
        report = self.__server.get_build_test_report(self.job_name, self.get_job_number())
        return report

    def get_jenkins_report(self):
        """统计测试报告用例成功数、失败数、跳过数以及成功率、失败率"""
        report = self.get_build_report()
        failCount = report["failCount"]
        passCount = report["passCount"]
        skipCount = report["skipCount"]
        totalcount = int(failCount) + int(passCount) + int(skipCount)
        duration = report["duration"]
        hour = duration // 3600
        minute = duration % 3600 // 60
        seconds = duration % 3600 % 60
        execute_duration = f'{hour}时{minute}分{seconds}秒'
        content = f'本次测试共执行{totalcount}个测试用例，成功：{passCount}个; 失败：{failCount}个; 跳过：{skipCount}个; 执行时长：{hour}时{minute}分{seconds}秒'
        # 提取测试报告链接
        console_log = self.get_console_log()
        # report_line = re.search(r'http://127.0.0.1:8090/job/api_test/(.*?)allure', console_log).group(0)
        report_info = {
            'total': totalcount,
            'pass_count': passCount,
            'fail_count': failCount,
            'skip_count': skipCount,
            'execute_duration': execute_duration,
            'report_line': "http://127.0.0.1:8090/job/api_test/allure/"
        }
        return report_info



if __name__ == '__main__':
    # print(JenkinsManege().get_job_number())
    # print(JenkinsManege().get_job_description())
    # print(JenkinsManege().get_build_job_status())
    # print(JenkinsManege().get_console_log())
    # print(JenkinsManege().get_build_report())
    print(JenkinsManege().get_jenkins_report())
    # print(JenkinsManege().get_console_log())
