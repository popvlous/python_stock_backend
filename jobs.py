import datetime

from flask import current_app

from app import app, config
from factory import sendActionRecordModel
from model import TPP_API_tppuser_behavior_v, TPP_API_tppuser_votepersons_v
from util import sendActionRecordByOne, lineNotifyMessage


def sendActionRecordJob():
    # 拋送資料
    with app.app_context():
        try:
            sendActionRecordModel(TPP_API_tppuser_behavior_v)
            sendActionRecordModel(TPP_API_tppuser_votepersons_v)
            current_app.logger.info(f'sendActionRecord 完成執行')
        except Exception as err:
            current_app.logger.error(f'sendActionRecord 發生錯誤: {err}')
