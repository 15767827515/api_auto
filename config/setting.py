import os

# 项目跟路径
ROOT_PATH=os.path.dirname(os.path.dirname(__file__))

# 保存关联变量的文件路径
extract_yanl_path=os.path.join(ROOT_PATH,"extract_var.yaml")

# 配置文件ini的路径
config_path=os.path.join(os.path.join(ROOT_PATH,"config"),"config.ini")


# print(config_path)