import os

import allure
import pytest

from config.setting import ROOT_PATH, testcase_path
from utils.request_control import RequestBase
from utils.yaml_control import read_test_yaml
from utils.generate_case_id import *

cwd_path=os.getcwd()

class TestInvoiceInspection:

    @pytest.mark.parametrize(('baseinfo,testdata'),
                             read_test_yaml(ROOT_PATH+r"\testcase\Invoice_Inspection\Invoice_Inspection.yaml"))
    def test_upload_file(self,baseinfo,testdata):
        RequestBase().request_base(baseinfo,testdata)

    @pytest.mark.smoke
    @pytest.mark.parametrize(('baseinfo,testdata'),
                             read_test_yaml(ROOT_PATH + r"\testcase\Invoice_Inspection\Invoice_upload.yaml"))
    def test_invoice_inspection(self, baseinfo, testdata):
        RequestBase().request_base(baseinfo, testdata)

