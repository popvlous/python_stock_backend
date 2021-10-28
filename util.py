import json
from datetime import datetime

import aiohttp
import requests
from flask import app, current_app

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
    headers = {
        "Content-Type": "application/json"

    }
    data_json = json.dumps(data_info)
    current_app.logger.error(f'{data_info.account}開始發送資料')
    try:
        response_info = requests.post(url, headers=headers, json=data_json)
    except Exception as error:
        current_app.logger.error(f'{data_info.account} call api address: {url} 發生錯誤: {error}')
        return 404
    if not response_info:
        return None
    else:
        order_details = json.loads(response_info.content.decode("utf-8").replace("'", '"'))
        return order_details