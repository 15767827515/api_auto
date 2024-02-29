import requests

from utils.read_config import ConfigParser


def send_enterprise_weChat_robot(message,at_all=False):
    url = ConfigParser.get_enterprise_weChat_robot_options("token_api")
    headers = {"Content-Type": "application/json"}
    if not at_all:
        data = {
            "msgtype": "text",
            "text": {
                "content": message,
                "mentioned_list": [],
                "mentioned_mobile_list": []
            }
        }
    elif at_all:
        data = {
            "msgtype": "text",
            "text": {
                "content": message,
                "mentioned_list": ["@all"],
                "mentioned_mobile_list": ["@all"]
            }
        }

    res = requests.post(url=url, headers=headers, json=data)
    return res.text



