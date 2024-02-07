import pytest

from utils.request_control import RequestBase
from utils.yaml_control import read_test_yaml


class TestLogin:

    @pytest.mark.parametrize(('baseinfo,testdata'),
                             read_test_yaml( r"D:\pytest-auto-api2-master\pytest-auto-api2-master\pythonProject\testcase\LoginAPI\login.yaml"))
    def test_user_login(self,baseinfo,testdata):
        RequestBase().request_base(baseinfo,testdata)


