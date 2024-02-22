import pytest

from config.setting import ROOT_PATH
from utils.request_control import RequestBase
from utils.yaml_control import read_test_yaml


class TestCrmLogin:

    @pytest.mark.parametrize(('baseinfo,testdata'),
                             read_test_yaml( ROOT_PATH+r"\testcase/CrmLogin/CrmLogin.yaml"))
    def test_crmlogin(self,baseinfo,testdata):
        RequestBase().request_base(baseinfo,testdata)