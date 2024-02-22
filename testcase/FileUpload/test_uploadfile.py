import allure
import pytest

from config.setting import ROOT_PATH
from utils.request_control import RequestBase
from utils.yaml_control import read_test_yaml



@allure.feature("合同文件上传模块")
class TestUploadfile:

    @pytest.mark.parametrize(('baseinfo,testdata'),
                             read_test_yaml( ROOT_PATH+r"\testcase\FileUpload\fileupload.yaml"))
    def test_upload_file(self,baseinfo,testdata):
        RequestBase().request_base(baseinfo,testdata)