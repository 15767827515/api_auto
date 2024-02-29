import os
import shutil

import sys
import pytest

if __name__ == "__main__":
    sys.argv = [
        sys.argv[0],  # 保留脚本名称
        '-s',  # 输出详细信息
        '-v',  # 详细输出
        '--alluredir=./report/temp',  # Allure 报告目录
        './testcase',  # 测试目录
        '--clean-alluredir', #  清理报告目录
        # "-k smoke",
        "--junitxml=./report/results.xml"
    ]

    pytest.main()
    shutil.copy('./environment.properties', './report/temp')  # 在Allure报告中添加环境信息
    # os.system(f'allure serve ./report/temp')
