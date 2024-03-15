import json
import os

import yaml
# from jsonschema import Draft7Validator, RefResolver
from googletrans import Translator

from config.setting import swagger_path, swagger_yaml_case_path


class SwaggerControl:

    def read_swagger_json(self):
        swagger_filepath = None
        for file in os.listdir(swagger_path):
            swagger_filepath = os.path.join(swagger_path, file)
        with open(swagger_filepath, "r", encoding="utf-8") as f:
            swagger_json_info = json.load(f)
            # swagger_json_info=JSON.parseObject(swagger_json_info, Feature.DisableCircularReferenceDetect);
        return swagger_json_info

    def resolve_refs(self, schema, base_uri):
        def resolve_refs(schema, base_uri):
            def _resolve_refs(schema, base_uri):
                # 检查schema是否为字典
                if isinstance(schema, dict):
                    # 递归处理字典中的每个键值对
                    return {k: _resolve_refs(v, base_uri) for k, v in schema.items()}
                # 检查schema是否为列表
                elif isinstance(schema, list):
                    # 递归处理列表中的每个元素
                    return [_resolve_refs(item, base_uri) for item in schema]
                elif '$ref' in schema:
                    # 如果是包含$ref的字典
                    ref = schema['$ref']
                    # 使用RefResolver解析引用
                    resolver = RefResolver(base_uri, ref)
                    resolved = resolver.resolve()
                    # 递归处理解析后的结果
                    return _resolve_refs(resolved, base_uri)
                else:
                    # 如果不是字典、列表或包含$ref的字典，则直接返回schema
                    return schema

            return _resolve_refs(schema, base_uri)

    def get_full_swagger_json_info(self):
        swagger_json_info = self.read_swagger_json()
        base_uri = ''
        full_swagger_json_info = self.resolve_refs(swagger_json_info, base_uri)
        return json.dumps(full_swagger_json_info, indent=2)

    def translate_to_english(self, text):
        translator = Translator()
        translation = translator.translate(text, dest='en')
        return translation.text

    def make_swagger_yaml_dir(self, api_name):
        word_list = []
        for word in self.translate_to_english(api_name).split(" "):
            word_list.append(str.capitalize(word))
        english_api_name = "_".join(word_list)
        swagger_yaml_path = os.path.join(swagger_yaml_case_path, english_api_name)
        if not os.path.exists(swagger_yaml_path):
            os.mkdir(swagger_yaml_path)
        return swagger_yaml_path, english_api_name

    def make_swagger_yaml_case_file(self):
        all_api_info_dict = self.read_swagger_json()["paths"]
        _dict = {}
        for url in all_api_info_dict.keys():
            for key, value in all_api_info_dict[url].items():
                feature_name = value.get("tags", [])[0]
                api_name = value.get("summary", [])
                header = value.get("header", [])
                method = key
                _parameters = value.get("parameters", [])
                for i in _parameters:
                    _dict[i['name']] = ""
                yaml_data = [{"baseInfo": {"feature_name": feature_name, "api_name": api_name, "url": url,
                                           "method": method, "header": header}},
                             {"testCase": [{"case_name": None, "paras": _dict}]}]
                swagger_yaml_path, english_api_name = self.make_swagger_yaml_dir(api_name)
                swagger_yaml_filepath = swagger_yaml_path + os.sep + english_api_name + ".yaml"
                print(swagger_yaml_filepath)
                with open(swagger_yaml_filepath, "w+", encoding="utf-8") as f:
                    yaml.dump(yaml_data, f, allow_unicode=True)


# if __name__ == '__main__':
    # print(SwaggerControl().make_swagger_yaml_case_file())

    # print(SwaggerControl().translate_to_english("获取销项发票信息列表"))
    # print(SwaggerControl().make_swagger_yaml_dir())
