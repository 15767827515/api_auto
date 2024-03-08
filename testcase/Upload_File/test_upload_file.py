
import allure
import pytest
from config.setting import ROOT_PATH
from utils.request_control import RequestBase
from utils.yaml_control import read_test_yaml

class TestUploadFile:

    @pytest.mark.parametrize(('baseinfo,testdata'),
                     read_test_yaml(r"D:\pytest-auto-api2-master\pytest-auto-api2-master\pythonProject\testdata\Upload_File\upload_file.yaml"))
    def test_upload_file(self,baseinfo,testdata):
        RequestBase().request_base(baseinfo,testdata)

