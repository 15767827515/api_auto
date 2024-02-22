# 用例前后置执行的代码
import pytest

from utils.extract_control import clean_extract_yaml


@pytest.fixture(scope="session", autouse=True)
def clean_extract_yaml_data():
    clean_extract_yaml()
