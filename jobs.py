from app import app
from model import Orders, db, OrdersLineItems, ViewDict
from util import sendActionRecordByOne


def sendActionRecordJob():
    # 拋送資料
    with app.app_context():
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
