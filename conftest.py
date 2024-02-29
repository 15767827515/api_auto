# 用例前后置执行的代码
import time

import pytest

from utils.Enterprise_WeChat_Robot import send_enterprise_weChat_robot
from utils.dingdingRobot import DingDingRobot
from utils.extract_control import clean_extract_yaml
from utils.jenkins_control import JenkinsManege
from utils.recordlog import logs


@pytest.fixture(scope="session", autouse=True)
def clean_extract_yaml_data():
    clean_extract_yaml()


# @pytest.fixture(scope="session", autouse=True)
# def send_dingding():
#     yield
#     res=DingDingRobot().send_dingding_request(1)
#     logs.info(f"测试结果发送到钉钉群的接口返回结果是：{res}")

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """生成测试结果摘要字符串"""
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error = len(terminalreporter.stats.get('error', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    duration = time.time() - terminalreporter._sessionstarttime

    # summary = f"""
    #     自动化测试结果，通知如下：
    #     测试用例总数：{total}
    #     测试通过数：{passed}
    #     测试失败数：{failed}
    #     错误数量：{error}
    #     跳过执行数量：{skipped}
    #     执行总时长：{duration}
    #     """
    summary = str(JenkinsManege().get_jenkins_report())
    if summary:
        dingding_res = DingDingRobot().send_dingding_request(summary,at_all=False)
        logs.info(f"测试结果发送到钉钉群的接口返回结果是：{dingding_res}")
        wechat_res = send_enterprise_weChat_robot(summary,at_all=False)
        logs.info(f"测试结果发送到企业微信群的接口返回结果是：{wechat_res}")
