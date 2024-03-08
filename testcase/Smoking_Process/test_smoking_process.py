
import allure
import pytest
from config.setting import ROOT_PATH
from utils.request_control import RequestBase
from utils.yaml_control import read_test_yaml

class TestSmokingProcess:

    @pytest.mark.parametrize(('baseinfo,testdata'),
                     read_test_yaml(r"D:\pytest-auto-api2-master\pytest-auto-api2-master\pythonProject\testdata\Smoking_Process\smoking_process.yaml"))
    def test_smoking_process(self,baseinfo,testdata):
        RequestBase().request_base(baseinfo,testdata)

