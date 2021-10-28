from flask import current_app

from app import app
from model import Orders, db, OrdersLineItems, ViewDict
from util import sendActionRecordByOne


def sendActionRecordJob():
    # 拋送資料
    with app.app_context():
        try:
            data = ViewDict.query.all()
            for data_info in data:
                data_json = {
                    "account": "",
                    "code": "",
                    "expandFlag": "",
                    "actionDate": "",
                    "token": ""
                }
                status = sendActionRecordByOne(data_json)
        except Exception as err:
            current_app.logger.error(f'{data_info.account } sendActionRecord 發生錯誤: {err}')
