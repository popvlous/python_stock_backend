import model
from app import config
from model import TPP_API_tppuser_behavior_v, TPP_API_tppuser_votepersons_v
from util import sendActionRecordSet


def sendActionRecordModel(t_name):
    if t_name == model.TPP_API_tppuser_behavior_v:
        data = TPP_API_tppuser_behavior_v.query.all()
        # data_json = {
        #     'account': '',
        #     'code': '',
        #     'expandFlag': '',
        #     'actionDate': '',
        #     'token': config.DATA_TOKEN
        # }
        status_code = sendActionRecordSet(data, t_name)
        return status_code
    elif t_name == model.TPP_API_tppuser_votepersons_v:
        data = TPP_API_tppuser_votepersons_v.query.all()
        status_code = sendActionRecordSet(data, t_name)
        return status_code
    else:
        return 404









