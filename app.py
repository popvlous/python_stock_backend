import logging
from logging.handlers import TimedRotatingFileHandler

import pymysql
from flask import Flask, jsonify, request, redirect
from flask.logging import default_handler
from config import config_dict
from model import db
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler


pymysql.install_as_MySQLdb()
scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))


# conn = MongoClient("mongodb://sds:Foxconn890@192.168.100.11:15017,192.168.100.12:15017,192.168.100.13:15017/sds")
# mongodb://<user_name>:<user_password>@ds<xxxxxx>.mlab.com:<xxxxx>/<database_name>
# db = conn.sds
# collection = db.users
# collection1 = db.inspections

# 正式環境請修正mode = 'Production'

mode = 'Debug'
app = Flask(__name__)
# app.config["SERVER_NAME"] = 'test.com:5000'

if mode == 'Production':
    config = config_dict['Production']
else:
    config = config_dict['Debug']

app.config.from_object(config)

print(config.SQLALCHEMY_DATABASE_URI)

# 移除預設的handler
app.logger.removeHandler(default_handler)
# 設定 Werkzeug logger 的等級，不顯示請求的log
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

formatter = logging.Formatter(
    '%(asctime)s [%(thread)d:%(threadName)s] [%(pathname)s:%(lineno)d] [%(levelname)s]: %(message)s')
handler = TimedRotatingFileHandler(
    "logs/flask.log", when="D", interval=1, backupCount=15,
    encoding="UTF-8", delay=False, utc=True)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

# 往螢幕上輸出
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
app.logger.addHandler(stream_handler)

if mode == 'Debug':
    app.logger.info('DBMS        = ' + config.SQLALCHEMY_DATABASE_URI)

db.init_app(app)
scheduler.init_app(app)
scheduler.start()


# 路由設定
# app.add_url_rule('/pcs/api/v1/inventories/<int:customer_id>', view_func=inventory)
# app.add_url_rule('/pcs/api/v1/inventory/history/<int:customer_id>', view_func=inventoryhistory)
# app.add_url_rule('/pcs/api/v1/inventory/delivery/history/<int:customer_id>', view_func=deliveryhistory)
# app.add_url_rule('/pcs/api/v1/inventory/add', methods=['GET', 'POST'], view_func=inventoryadd)
# app.add_url_rule('/pcs/api/v1/inventory/delivery', methods=['GET', 'POST'], view_func=inventorydelivery)
# app.add_url_rule('/pcs/api/v1/inventory/deliveries', methods=['GET', 'POST'], view_func=inventorydeliveries)


# @app.route('/', subdomain="admin")
@app.route('/')
def hello_world():
    return redirect('https://storeapi.pyrarc.com/backend/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
