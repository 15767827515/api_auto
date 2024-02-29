import requests

from utils.read_config import ConfigParser


def send_enterprise_weChat_robot(message,at_all=True):
    url = ConfigParser.get_enterprise_weChat_robot_options("token_api")
    headers = {"Content-Type": "application/json"}

    if not at_all:
        data = {
            "msgtype": "text",
            "text": {
                "content": message,
                "mentioned_list": ["15767827515"],
                "mentioned_mobile_list": ["15767827515"]
            }
        }
        res = requests.post(url=url, headers=headers, json=data)
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


