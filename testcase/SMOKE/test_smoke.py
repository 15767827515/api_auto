import os

import allure
import pytest

from config.setting import ROOT_PATH, testcase_path
from utils.request_control import RequestBase
from utils.yaml_control import read_test_yaml
from utils.generate_case_id import *

cwd_path=os.getcwd()

class TestSmoke:



    @pytest.mark.parametrize(('baseinfo,testdata'),
                             read_test_yaml(ROOT_PATH + r"\testcase\SMOKE\smoke.yaml"))
    def test_smoke(self, baseinfo, testdata):
        RequestBase().request_base(baseinfo, testdata)

