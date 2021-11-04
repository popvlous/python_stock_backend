import datetime

from flask import current_app

from app import app, config
from model import TPP_API_tppuser_behavior_v
from util import sendActionRecordByOne, lineNotifyMessage


def sendActionRecordJob():
    # 拋送資料
    with app.app_context():
        try:
            data = TPP_API_tppuser_behavior_v.query.all()
            current_app.logger.info( f' 共 {len(data)} 筆，開始拋送資料 ')
            lineNotifyMessage(config.LINE_TOKEN, f' 溫馨提醒: Mysql 共 {len(data)} 筆，開始拋送資料 ')
            for data_info in data:
                data_json = {
                    'account': data_info.account,
                    'code': data_info.code,
                    'expandFlag': '',
                    'actionDate': data_info.actionDate[:10],
                    'token': config.DATA_TOKEN
                }
                status = sendActionRecordByOne(data_json)
                if status["code"] == "00000":
                    current_app.logger.info(
                        f' {data_info.account} 拋送資料成功 code: {status["code"]} data: {status["data"]}')
                else:
                    current_app.logger.error(
                        f' {data_info.account} 拋送資料發生錯誤 code: {status["code"]} message: {status["message"]}')
            lineNotifyMessage(config.LINE_TOKEN, f' 溫馨提醒: Mysql 共 {len(data)} 筆，拋送資料完畢 ')
        except Exception as err:
            current_app.logger.error(f'sendActionRecord 發生錯誤: {err}')
