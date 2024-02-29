import time
import hmac
import hashlib
import base64
import urllib.parse

import requests

from utils.read_config import ConfigParser


class DingDingRobot:

    def generate_dingding_sign(self):
        timestamp = str(round(time.time() * 1000))
        secret = ConfigParser.get_dingdingrobot_options("secret")
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign

    def send_dingding_request(self, content_str, at_all=True):
        timestamp, sign = self.generate_dingding_sign()
        url = ConfigParser.get_dingdingrobot_options("token_api") + f"&timestamp={timestamp}&sign={sign}"
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "msgtype": "text",
            "text": {
                "content": content_str
            },
            "at": {
                "isAtAll": at_all
            }, }
        res = requests.post(url, json=data, headers=headers)
        return res.text



if __name__ == '__main__':
    DingDingRobot().send_dingding_request(1,at_all=False)
