import json
from datetime import datetime

import requests
from flask import app, current_app

from app import config

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
    url = config.DOMAIN_URL + "api/actionRecord"
    headers = {
        "Content-Type": "application/json"

    }
    # data_json = json.dumps(data_info, default=defaultconverter)
    # data = {
    #     'account': 'popvlous',
    #     'code': '00001',
    #     'expandFlag': '',
    #     'actionDate': '2021-11-02',
    #     'token': 'ENXsCAbfyXYqincPulKe'
    # }
    current_app.logger.info(f'sendActionRecordByOne 開始發送資料')
    try:
        response_info = requests.post(url, headers=headers, json=data_info)
    except Exception as error:
        current_app.logger.error(f'{data_info.account} call api address: {url} 發生錯誤: {error}')
        return 404
    if not response_info:
        return None
    else:
        response_details = json.loads(response_info.content.decode("utf-8").replace("'", '"'))
        return response_details

def defaultconverter(o):
    if isinstance(o, datetime):
        return o.__str__()