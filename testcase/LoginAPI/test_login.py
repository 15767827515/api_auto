import pytest

from config.setting import extract_yanl_path, ROOT_PATH
from utils.request_control import RequestBase
from utils.yaml_control import read_test_yaml


class TestLogin:

    @pytest.mark.parametrize(('baseinfo,testdata'),
                             read_test_yaml( ROOT_PATH+r"\testcase\LoginAPI\login.yaml"))
    def test_user_login(self,baseinfo,testdata):
        RequestBase().request_base(baseinfo,testdata)


