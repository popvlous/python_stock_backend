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


def sendActionRecordSet(data, t_name):
    try:
        current_app.logger.info( f' {t_name} 共 {len(data)} 筆，開始拋送資料 ')
        lineNotifyMessage(config.LINE_TOKEN, f' {t_name} 溫馨提醒: Mysql 共 {len(data)} 筆，開始拋送資料 ')
        for data_info in data:
            data_json = {
                'account': data_info.account,
                'code': data_info.code,
                'expandFlag': '',
                'actionDate': data_info.actionDate.strftime('%Y-%m-%dT%H:%M:%S') if isinstance(data_info.actionDate, datetime) else data_info.actionDate,
                'token': config.DATA_TOKEN
            }
            current_app.logger.info(f' 資料: {data_json}')
            status = sendActionRecordByOne(data_json)
            if status["code"] == "00000":
                current_app.logger.info(
                    f' {data_info.account} 拋送資料成功 code: {status["code"]} data: {status["data"]}')
            else:
                current_app.logger.error(
                    f' {data_info.account} 拋送資料發生錯誤 code: {status["code"]} message: {status["message"]}')
        lineNotifyMessage(config.LINE_TOKEN, f' 溫馨提醒: Mysql {t_name} 共 {len(data)} 筆，拋送資料完畢 ')
        return 200
    except Exception as err:
        current_app.logger.error(f' {t_name} sendActionRecord 發生錯誤: {err}')
        return 404

def defaultconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,  # 權杖，Bearer 的空格不要刪掉呦
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}

    # Post 封包出去給 Line Notify
    r = requests.post(
        "https://notify-api.line.me/api/notify",
        headers=headers,
        params=payload)
    return r.status_code