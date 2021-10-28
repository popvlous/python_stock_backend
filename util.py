import json
from datetime import datetime

import aiohttp
import requests
from flask import app

from model import Orders

token = "SEY3QW9ES2ZBbw=="

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
}

user_name = "pyrarc.app"
user_passwd = "B8I%7s2MnQ1&nTM9OYP15ms0"
end_point_url_posts = "https://store.pyrarc.com/wp-json/jwt-auth/v1/token"

payload = {
    "username": user_name,
    "password": user_passwd
}


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def sendActionRecordByOne(data_info):
    url = "https://member-api.tpp.org.tw/api/actionRecord"
    response_info = requests.post(url, data=data_info)

    if not response_info:
        return None
    order_details = json.loads(response_info.content.decode("utf-8").replace("'", '"'))
    return order_details
