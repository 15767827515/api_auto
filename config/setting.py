import os

# 项目跟路径
ROOT_PATH=os.path.dirname(os.path.dirname(__file__))

# 保存关联变量的文件路径
extract_yanl_path=os.path.join(ROOT_PATH,"extract_var.yaml")

# 配置文件ini的路径
config_path=os.path.join(os.path.join(ROOT_PATH,"config"),"config.ini")

# 公钥文件public_key.pem路径
public_key_path=os.path.join(ROOT_PATH,"public_key.pem")

testcase_path=os.path.join(ROOT_PATH,"testcase")


# print(config_path)
# print(testcase_path)
