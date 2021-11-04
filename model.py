import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ViewDict(db.Model):
    __viewname__ = 'view_dict'
    dic_key = db.Column(db.Integer, primary_key=True)
    dic_name = db.Column(db.String(50))
    dic_sort_code = db.Column(db.String(50))
    dic_sort = db.Column(db.String(50))
    dic_sort_id = db.Column(db.Integer)
    dic_remark = db.Column(db.String(500))

    def __init__(self, dic_key, dic_name, dic_sort_code, dic_sort, dic_sort_id, dic_remark):
        self.dic_key = dic_key
        self.dic_name = dic_name
        self.dic_sort_code = dic_sort_code
        self.dic_sort = dic_sort
        self.dic_sort_id = dic_sort_id
        self.dic_remark = dic_remark

    def to_json(self):
        return {
            'dic_key': self.dic_key,
            'dic_name': self.dic_name,
            'dic_sort_code': self.dic_sort_code,
            'dic_sort': self.dic_sort,
            'dic_sort_id': self.dic_sort_id,
            'dic_remark': self.dic_remark
        }


class TPP_API_tppuser_behavior_v(db.Model):
    __viewname__ = 'TPP_API_tppuser_behavior_v'
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(50))
    code = db.Column(db.String(50))
    actionDate = db.Column(db.String(50))

    def __init__(self, id, account, code, actionDate):
        self.id = id
        self.account = account
        self.code = code
        self.actionDate = actionDate

    def to_json(self):
        return {
            'id': self.id,
            'account': self.account,
            'code': self.code,
            'actionDate': self.actionDate
        }