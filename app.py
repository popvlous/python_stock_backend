import asyncio
import json
import logging
from logging.handlers import TimedRotatingFileHandler
from sched import scheduler

import pymysql
import requests
from flask import Flask, jsonify, request, redirect
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from woocommerce import API
from config import config_dict
from inventory import inventory, inventoryadd, getInvertoryNow, inventorydelivery, inventoryhistory, \
    inventorydeliveries, deliveryhistory
from model import db, Orders, OrdersLineItems, Inventory
from util import insertBlockChainOrder, insertBlockChainInventory, insertBlockChainLineItem, updateBlockChainOrder, \
    updateBlockChainLineItem, updateBlockChainInventory, getOrderDetail, insertBlockChainOrderAsync
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler


pymysql.install_as_MySQLdb()
scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))


# conn = MongoClient("mongodb://sds:Foxconn890@192.168.100.11:15017,192.168.100.12:15017,192.168.100.13:15017/sds")
# mongodb://<user_name>:<user_password>@ds<xxxxxx>.mlab.com:<xxxxx>/<database_name>
# db = conn.sds
# collection = db.users
# collection1 = db.inspections


# woocommerce api
wcapi = API(
    url="https://store.pyrarc.com",
    consumer_key="ck_ab98c184df28b6bc3298710a139177b00564a302",
    consumer_secret="cs_9de359730bb8aa8d4faf3395541c503e90997294",
    version="wc/v3"
)

user_name = "pyrarc.app"
user_passwd = "B8I%7s2MnQ1&nTM9OYP15ms0"
end_point_url_posts = "https://store.pyrarc.com/wp-json/jwt-auth/v1/token"

payload = {
    "username": user_name,
    "password": user_passwd
}

# 區塊鏈基礎訊息
token = "SEY3QW9ES2ZBbw=="
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
}

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
app.add_url_rule('/pcs/api/v1/inventories/<int:customer_id>', view_func=inventory)
app.add_url_rule('/pcs/api/v1/inventory/history/<int:customer_id>', view_func=inventoryhistory)
app.add_url_rule('/pcs/api/v1/inventory/delivery/history/<int:customer_id>', view_func=deliveryhistory)
app.add_url_rule('/pcs/api/v1/inventory/add', methods=['GET', 'POST'], view_func=inventoryadd)
app.add_url_rule('/pcs/api/v1/inventory/delivery', methods=['GET', 'POST'], view_func=inventorydelivery)
app.add_url_rule('/pcs/api/v1/inventory/deliveries', methods=['GET', 'POST'], view_func=inventorydeliveries)


# @app.route('/', subdomain="admin")
@app.route('/')
def hello_world():
    return redirect('https://storeapi.pyrarc.com/backend/login')


@app.route('/pcs/api/v1/product', methods=['GET', 'POST'])
def show():
    # !/usr/bin/python
    # -*- coding: utf-8 -*-
    ##headers = {'content-type': "application/x-www-form-urlencoded"}
    r = requests.post(end_point_url_posts, data=payload)
    jwt_info = r.content.decode("utf-8").replace("'", '"')
    data = json.loads(jwt_info)
    s = json.dumps(data, indent=4, sort_keys=True)
    print(s)
    token = data['token']
    Auth_token = "Bearer " + token

    my_headers = {'Authorization': Auth_token}

    # productlist = wcapi.get("products", params={"per_page": 20}).json()

    response_productlist = requests.get('https://store.pyrarc.com/wp-json/wc/v3/products', data=payload,
                                        headers=my_headers)
    productlist = json.loads(response_productlist.content.decode("utf-8").replace("'", '"'))
    print(productlist)

    return jsonify({
        'success': True,
        'msg': 'product list is {} '.format(productlist)
    })


@app.route('/pcs/api/v1/customer', methods=['GET', 'POST'])
def showcustomers():
    # !/usr/bin/python
    # -*- coding: utf-8 -*-
    ##headers = {'content-type': "application/x-www-form-urlencoded"}
    r = requests.post(end_point_url_posts, data=payload)
    jwt_info = r.content.decode("utf-8").replace("'", '"')
    data = json.loads(jwt_info)
    s = json.dumps(data, indent=4, sort_keys=True)
    print(s)
    token = data['token']
    Auth_token = "Bearer " + token

    my_headers = {'Authorization': Auth_token}

    # productlist = wcapi.get("products", params={"per_page": 20}).json()

    response_customers = requests.get('https://store.pyrarc.com/wp-json/wc/v3/customers', data=payload,
                                      headers=my_headers)
    customerlist = json.loads(response_customers.content.decode("utf-8").replace("'", '"'))
    print(customerlist)

    return jsonify({
        'success': True,
        'msg': 'product list is {} '.format(customerlist)
    })


# 獲取單所有用戶的用戶訂單訊息
@app.route('/pcs/api/v1/order')
def showorders():
    orders = Orders.query.filter().all()
    json_format = json.dumps(orders)
    print(json_format)
    return jsonify({
        'success': True,
        'msg': 'orders list is {} '.format(json_format)
    })


# 獲取單一用戶所有訂單訊息
@app.route('/pcs/api/v1/order/<int:customer_id>')
def showorder(customer_id: int):
    order_infos = []
    orders = Orders.query.filter_by(customer_id=customer_id).all()

    if orders:
        return jsonify([order.to_json() for order in orders])
    else:
        return jsonify({
            'message': 'data is not exist'
        })


# 獲取單一用戶所有訂單區塊鏈訊息
@app.route('/pcs/api/v1/order/bc/<int:customer_id>')
def showbcorder(customer_id: int):
    order_infos = []
    orders = Orders.query.filter_by(customer_id=customer_id).all()

    if orders:
        # productlist = wcapi.get("products", params={"per_page": 20}).json()
        for order in orders:
            response_orderlist = requests.get(
                'https://ccapi.stag.nexuera.com/orders/query/' + str(order.order_id), headers=headers, verify=False)
            # productlist = json.loads(response_orderlist.content.decode("utf-8").replace("'", '"'))
            if len(response_orderlist.content) == 0:
                order.checkinfo = False
            else:
                order.checkinfo = True
        return jsonify([order.to_json_ext() for order in orders])
    else:
        return jsonify({
            'message': 'data is not exist'
        })


# 獲取單一用戶單一訂單訂單區塊鏈訊息
@app.route('/pcs/api/v1/order/bc/<int:customer_id>/<int:order_id>')
def showbcorderone(customer_id=None, order_id=None):
    orders = Orders.query.filter_by(customer_id=customer_id, order_id=order_id).all()

    if orders:
        # productlist = wcapi.get("products", params={"per_page": 20}).json()
        for order in orders:
            response_orderlist = requests.get(
                'https://ccapi.stag.nexuera.com/orders/query/' + str(order.order_id), headers=headers, verify=False)
            # productlist = json.loads(response_orderlist.content.decode("utf-8").replace("'", '"'))
            if len(response_orderlist.content) == 0:
                order.checkinfo = False
            else:
                order.checkinfo = True
        return jsonify([order.to_json_ext() for order in orders])
    else:
        return jsonify({
            'message': 'data is not exist'
        })


@app.route('/pcs/api/v1/bc', methods=['POST'])
def order_details():
    request_data = request.data.decode('utf-8')
    if not request_data:
        return jsonify({
            'success': False
        })

    # 本機測試時請打開
    # j_request_data = json.loads(request_data)
    # req_id = j_request_data['id']
    # orderid = 'orders/' + str(req_id)
    # # 無jwt調用方式
    # # order_details = wcapi.get(orderid).json()
    # r = requests.post(end_point_url_posts, data=payload)
    # jwt_info = r.content.decode("utf-8").replace("'", '"')
    # data = json.loads(jwt_info)
    # my_headers = {'Authorization': "Bearer " + data['token']}
    # res_order_details = requests.get('https://store.pyrarc.com/wp-json/wc/v3/orders/' + str(req_id), data=payload,
    #                                  headers=my_headers)
    # order_details = json.loads(res_order_details.content.decode("utf-8").replace("'", '"'))

    # 正式環境webhook可以直接獲取到
    order_details = json.loads(request_data)
    order_details_id = order_details['id']
    order_details_parent_id = order_details['parent_id']
    order_details_status = order_details['status']
    order_details_currency = order_details['currency']
    order_details_version = order_details['version']
    order_details_date_created = order_details['date_created']
    order_details_date_modified = order_details['date_modified']
    order_details_total = order_details['total']
    order_details_total_tax = order_details['total_tax']
    order_details_payment_method = order_details['payment_method']
    order_details_payment_method_title = order_details['payment_method_title']
    order_details_transaction_id = order_details['transaction_id']
    order_details_customer_ip_address = order_details['customer_ip_address']
    order_details_created_via = order_details['created_via']
    order_details_customer_id = order_details['customer_id']
    order_details_customer_note = order_details['customer_note']
    order_details_cart_hash = order_details['cart_hash']

    # 保存billing訊息
    billing = order_details['billing']
    billing_first_name = billing['first_name']
    billing_last_name = billing['last_name']
    billing_company = billing['company']
    billing_address_1 = billing['address_1']
    billing_address_2 = billing['address_2']
    billing_city = billing['city']
    billing_state = billing['state']
    billing_postcode = billing['postcode']
    billing_country = billing['country']
    billing_email = billing['email']
    billing_phone = billing['phone']
    # 保存shipping訊息
    shipping = order_details['shipping']
    shipping_first_name = shipping['first_name']
    shipping_last_name = shipping['last_name']
    shipping_company = shipping['company']
    shipping_address_1 = shipping['address_1']
    shipping_address_2 = shipping['address_2']
    shipping_city = shipping['city']
    shipping_state = shipping['state']
    shipping_postcode = shipping['postcode']
    shipping_country = shipping['country']
    # 保存line items
    line_items = order_details['line_items']
    # line_items_id = line_items['id']
    # line_items_name = line_items['name']
    # line_items_product_id = line_items['product_id']
    # line_items_variation_id = line_items['variation_id']
    # line_items_quantity = line_items['quantity']
    # line_items_tax_class = line_items['tax_class']
    # line_items_subtotal = line_items['subtotal']
    # line_items_subtotal_tax = line_items['subtotal_tax']
    # line_items_total = line_items['total']
    # line_items_total_tax = line_items['total_tax']
    # line_items_taxes = line_items['taxes']
    # line_items_sku = line_items['sku']
    # line_items_price = line_items['price']
    # line_items_parent_name = line_items['parent_name']

    # 保存資料庫
    order_info = Orders(order_details_id, order_details_parent_id, order_details_status, billing_first_name,
                        billing_last_name, order_details_currency, order_details_version, order_details_total,
                        order_details_total_tax,
                        billing_company, billing_address_1, billing_address_2, billing_city, billing_state,
                        billing_postcode, billing_country, billing_email, billing_phone, shipping_first_name,
                        shipping_last_name, shipping_company, shipping_address_1, shipping_address_2, shipping_city,
                        shipping_state,
                        shipping_postcode, shipping_country, order_details_payment_method,
                        order_details_payment_method_title, order_details_transaction_id,
                        order_details_customer_ip_address, order_details_created_via, order_details_customer_id,
                        order_details_customer_note, order_details_cart_hash)
    db.session.add(order_info)
    db.session.commit()
    # bc_info = insertBlockChainOrder(order_details)
    # print(bc_info)
    # tx_id = ''
    # if int(bc_info[0]) == 200:
    #     tx_id = bc_info[1].decode("utf-8").replace("'", '"')
    # else:
    #     tx_id = bc_info[0]
    # print(tx_id)
    # #   更新tx
    #修正使用排程上鏈，避免付款問題
    order_info_tx = Orders.query.filter_by(id=order_info.id).one()
    order_info_tx.tx_id = "0"
    db.session.commit()

    # 保存資料庫

    for line_item in line_items:
        line_items_id = line_item['id']
        line_items_name = line_item['name']
        line_items_product_id = line_item['product_id']
        line_items_variation_id = line_item['variation_id']
        line_items_quantity = line_item['quantity']
        line_items_tax_class = line_item['tax_class']
        line_items_subtotal = line_item['subtotal']
        line_items_subtotal_tax = line_item['subtotal_tax']
        line_items_total = line_item['total']
        line_items_total_tax = line_item['total_tax']
        line_items_taxes = line_item['taxes']
        line_items_sku = line_item['sku']
        line_items_price = line_item['price']
        line_items_parent_name = line_item['parent_name']
        line_items_info = OrdersLineItems(order_details_id, line_items_id, line_items_name,
                                          line_items_product_id, line_items_variation_id, line_items_quantity,
                                          line_items_tax_class, line_items_subtotal, line_items_subtotal_tax,
                                          line_items_total,
                                          line_items_total_tax, line_items_sku, line_items_price,
                                          line_items_parent_name)
        db.session.add(line_items_info)
        db.session.commit()
        # line_item_bc_info = insertBlockChainLineItem(line_items_info)
        # print(line_item_bc_info)
        # line_item_tx_id = ''
        # if int(line_item_bc_info[0]) == 200:
        #     line_item_tx_id = line_item_bc_info[1].decode("utf-8").replace("'", '"')
        # else:
        #     line_item_tx_id = line_item_bc_info[0]
        # #   更新tx
        # line_items_info_tx = OrdersLineItems.query.filter_by(id=line_items_info.id).one()
        line_items_info_tx = OrdersLineItems.query.filter_by(id=line_items_info.id).one()
        line_items_info_tx.tx_id = "0"
        db.session.commit()

        # sql = "INSERT INTO Orders (order_id, parent_id, status, billing_first_name, billing_last_name)VALUES (" + str(
        #     order_details_id) + ", " + "" + str(order_details_parent_id) + ", " + str(order_details_status) + ", " + str(
        #     billing_first_name) + ", " + str(billing_last_name) + ")"
        # sql = 'INSERT INTO orders (order_id, parent_id, state, billing_first_name, billing_last_name, currency, date_created, date_modified, total, total_tax, payment_method, payment_method_title, transaction_id, customer_ip_address, created_via, customer_note, cart_hash, billing_company, billing_address_1 ,billing_address_2, billing_city, billing_state, billing_postcode, billing_country, billing_email, billing_phone, shipping_first_name, shipping_last_name, shipping_company, shipping_address_1, shipping_address_2, shipping_city, shipping_postcode, shipping_country )VALUES ({}, {}, {}, {}, {}, {}, NOW(), NOW(), {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(
        #     order_details_id,
        #     order_details_parent_id,
        #     "'" + order_details_status + "'",
        #     "'" + billing_first_name + "'",
        #     "'" + billing_last_name + "'",
        #     "'" + order_details_currency + "'",
        #     # datetime.strptime(order_details_date_created, '%Y-%m-%dT%H:%M:%S'),
        #     # datetime.strptime(order_details_date_modified, '%Y-%m-%dT%H:%M:%S'),
        #     order_details_total,
        #     order_details_total_tax,
        #     "'" + order_details_payment_method + "'",
        #     "'" + order_details_payment_method_title + "'",
        #     "'" + order_details_transaction_id + "'",
        #     "'" + order_details_customer_ip_address + "'",
        #     "'" + order_details_created_via + "'",
        #     "'" + order_details_customer_note + "'",
        #     "'" + order_details_cart_hash + "'",
        #     "'" + billing_company + "'",
        #     "'" + billing_address_1 + "'",
        #     "'" + billing_address_2 + "'",
        #     "'" + billing_city + "'",
        #     "'" + billing_state + "'",
        #     "'" + billing_postcode + "'",
        #     "'" + billing_country + "'",
        #     "'" + billing_email + "'",
        #     "'" + billing_phone + "'",
        #     "'" + shipping_first_name + "'",
        #     "'" + shipping_last_name + "'",
        #     "'" + shipping_company + "'",
        #     "'" + shipping_address_1 + "'",
        #     "'" + shipping_address_2 + "'",
        #     "'" + shipping_city + "'",
        #     # "'" + shipping_state + "'",
        #     "'" + shipping_postcode + "'",
        #     "'" + shipping_country + "'"
        # )
        # db.engine.execute(sql)

    print(jsonify(order_details))
    return jsonify({
        'success': True,
        'msg': 'order record is create in blcokchain ',
        'data': order_details
    })


@app.route('/pcs/api/v1/bc/update', methods=['POST'])
def orderupdate():
    request_data = request.data.decode('utf-8')
    if not request_data:
        return jsonify({
            'success': False
        })

    # 本機測試時請打開
    # j_request_data = json.loads(request_data)
    # req_id = j_request_data['id']
    # orderid = 'orders/' + str(req_id)
    # #無jwt調用方式
    # #order_details = wcapi.get(orderid).json()
    # r = requests.post(end_point_url_posts, data=payload)
    # jwt_info = r.content.decode("utf-8").replace("'", '"')
    # data = json.loads(jwt_info)
    # my_headers = {'Authorization': "Bearer " + data['token']}
    # res_order_details = requests.get('https://store.pyrarc.com/wp-json/wc/v3/orders/' + str(req_id), data=payload,
    #                                  headers=my_headers)
    # order_details = json.loads(res_order_details.content.decode("utf-8").replace("'", '"'))

    # 正式環境webhook可以直接獲取到
    order_details = json.loads(request_data)
    order_details_id = order_details['id']
    order_details_parent_id = order_details['parent_id']
    order_details_status = order_details['status']
    order_details_currency = order_details['currency']
    order_details_version = order_details['version']
    order_details_date_created = order_details['date_created']
    order_details_date_modified = order_details['date_modified']
    order_details_total = order_details['total']
    order_details_total_tax = order_details['total_tax']
    order_details_payment_method = order_details['payment_method']
    order_details_payment_method_title = order_details['payment_method_title']
    order_details_transaction_id = order_details['transaction_id']
    order_details_customer_ip_address = order_details['customer_ip_address']
    order_details_created_via = order_details['created_via']
    order_details_customer_id = order_details['customer_id']
    order_details_customer_note = order_details['customer_note']
    order_details_cart_hash = order_details['cart_hash']

    # 保存billing訊息
    billing = order_details['billing']
    billing_first_name = billing['first_name']
    billing_last_name = billing['last_name']
    billing_company = billing['company']
    billing_address_1 = billing['address_1']
    billing_address_2 = billing['address_2']
    billing_city = billing['city']
    billing_state = billing['state']
    billing_postcode = billing['postcode']
    billing_country = billing['country']
    billing_email = billing['email']
    billing_phone = billing['phone']
    # 保存shipping訊息
    shipping = order_details['shipping']
    shipping_first_name = shipping['first_name']
    shipping_last_name = shipping['last_name']
    shipping_company = shipping['company']
    shipping_address_1 = shipping['address_1']
    shipping_address_2 = shipping['address_2']
    shipping_city = shipping['city']
    shipping_state = shipping['state']
    shipping_postcode = shipping['postcode']
    shipping_country = shipping['country']
    # 保存line items
    line_items = order_details['line_items']
    # line_items_id = line_items['id']
    # line_items_name = line_items['name']
    # line_items_product_id = line_items['product_id']
    # line_items_variation_id = line_items['variation_id']
    # line_items_quantity = line_items['quantity']
    # line_items_tax_class = line_items['tax_class']
    # line_items_subtotal = line_items['subtotal']
    # line_items_subtotal_tax = line_items['subtotal_tax']
    # line_items_total = line_items['total']
    # line_items_total_tax = line_items['total_tax']
    # line_items_taxes = line_items['taxes']
    # line_items_sku = line_items['sku']
    # line_items_price = line_items['price']
    # line_items_parent_name = line_items['parent_name']

    # 保存資料庫
    # 訂單取消
    if order_details_status == 'cancelled':
        order_info = Orders(order_details_id, order_details_parent_id, order_details_status, billing_first_name,
                            billing_last_name, order_details_currency, order_details_version, order_details_total,
                            order_details_total_tax,
                            billing_company, billing_address_1, billing_address_2, billing_city, billing_state,
                            billing_postcode, billing_country, billing_email, billing_phone, shipping_first_name,
                            shipping_last_name, shipping_company, shipping_address_1, shipping_address_2, shipping_city,
                            shipping_postcode,
                            shipping_postcode, shipping_country, order_details_payment_method,
                            order_details_payment_method_title, order_details_transaction_id,
                            order_details_customer_ip_address, order_details_created_via, order_details_customer_id,
                            order_details_customer_note, order_details_cart_hash)
        db.session.add(order_info)
        db.session.commit()
        bc_order_details_cancelled = updateBlockChainOrder(order_details)
        print("cancelled")
        print(bc_order_details_cancelled)
        if int(bc_order_details_cancelled[0]) == 200:
            tx_id = bc_order_details_cancelled[1].decode("utf-8").replace("'", '"')
        else:
            tx_id = bc_order_details_cancelled[0]
        print(tx_id)
        #   更新tx
        order_info_tx = Orders.query.filter_by(id=order_info.id).one()
        if tx_id:
            order_info_tx.tx_id = tx_id
        db.session.commit()
        # 保存資料庫

        for line_item in line_items:
            line_items_id = line_item['id']
            line_items_name = line_item['name']
            line_items_product_id = line_item['product_id']
            line_items_variation_id = line_item['variation_id']
            line_items_quantity = line_item['quantity']
            line_items_tax_class = line_item['tax_class']
            line_items_subtotal = line_item['subtotal']
            line_items_subtotal_tax = line_item['subtotal_tax']
            line_items_total = line_item['total']
            line_items_total_tax = line_item['total_tax']
            line_items_taxes = line_item['taxes']
            line_items_sku = line_item['sku']
            line_items_price = line_item['price']
            line_items_parent_name = line_item['parent_name']
            line_items_info = OrdersLineItems(order_details_id, line_items_id, line_items_name,
                                              line_items_product_id, line_items_variation_id, line_items_quantity,
                                              line_items_tax_class, line_items_subtotal, line_items_subtotal_tax,
                                              line_items_total,
                                              line_items_total_tax, line_items_sku, line_items_price,
                                              line_items_parent_name)
            db.session.add(line_items_info)
            db.session.commit()
            line_item_bc_info = updateBlockChainLineItem(line_items_info)
            print(line_item_bc_info)
            if int(line_item_bc_info[0]) == 200:
                line_item_tx_id = line_item_bc_info[1].decode("utf-8").replace("'", '"')
            else:
                line_item_tx_id = line_item_bc_info[0]
            #   更新tx
            line_items_info_tx = OrdersLineItems.query.filter_by(id=line_items_info.id).one()
            if line_item_tx_id:
                line_items_info_tx.tx_id = line_item_tx_id
            db.session.commit()
            # 庫存異動 取消時的庫存異動，須先判斷原訂單庫存是否存在
            inventory_info = Inventory.query.filter_by(user_id=order_details_customer_id,
                                                       product_id=line_items_product_id,
                                                       order_id=order_details_id).limit(1).all()
            if inventory_info:
                beging_inventory, ending_inventory = getInvertoryNow(order_details_customer_id, line_items_product_id,
                                                                     line_items_quantity * -1)
                inventory = Inventory(order_details_customer_id, beging_inventory, ending_inventory,
                                      line_items_quantity * -1,
                                      order_details_id, line_items_product_id, 'System',
                                      'Web', '', '', '', '', '', '', '', '', '', 0)
                db.session.add(inventory)
                db.session.commit()
                inventory_bc_info = updateBlockChainInventory(inventory)
                print('inventory_cancelled')
                print(inventory_bc_info)
                if int(inventory_bc_info[0]) == 200:
                    inventory_tx_id = inventory_bc_info[1].decode("utf-8").replace("'", '"')
                else:
                    inventory_tx_id = inventory_bc_info[0]
                #   更新tx
                inventory_info_tx = Inventory.query.filter_by(id=inventory.id).one()
                if inventory_tx_id:
                    inventory_info_tx.tx_id = inventory_tx_id
                db.session.commit()
    # 訂單付款完成，增加庫存
    elif order_details_status == 'completed':
        order_info = Orders(order_details_id, order_details_parent_id, order_details_status, billing_first_name,
                            billing_last_name, order_details_currency, order_details_version, order_details_total,
                            order_details_total_tax,
                            billing_company, billing_address_1, billing_address_2, billing_city, billing_state,
                            billing_postcode, billing_country, billing_email, billing_phone, shipping_first_name,
                            shipping_last_name, shipping_company, shipping_address_1, shipping_address_2, shipping_city,
                            shipping_state,
                            shipping_postcode, shipping_country, order_details_payment_method,
                            order_details_payment_method_title, order_details_transaction_id,
                            order_details_customer_ip_address, order_details_created_via, order_details_customer_id,
                            order_details_customer_note, order_details_cart_hash)
        db.session.add(order_info)
        db.session.commit()
        bc_order_details_complete = updateBlockChainOrder(order_details)
        print("complete")
        print(bc_order_details_complete)
        if int(bc_order_details_complete[0]) == 200:
            tx_id = bc_order_details_complete[1].decode("utf-8").replace("'", '"')
        else:
            tx_id = bc_order_details_complete[0]
        print(tx_id)
        #   更新tx
        order_info_tx = Orders.query.filter_by(id=order_info.id).one()
        if tx_id:
            order_info_tx.tx_id = tx_id
        db.session.commit()

        for line_item in line_items:
            line_items_id = line_item['id']
            line_items_name = line_item['name']
            line_items_product_id = line_item['product_id']
            line_items_variation_id = line_item['variation_id']
            line_items_quantity = line_item['quantity']
            line_items_tax_class = line_item['tax_class']
            line_items_subtotal = line_item['subtotal']
            line_items_subtotal_tax = line_item['subtotal_tax']
            line_items_total = line_item['total']
            line_items_total_tax = line_item['total_tax']
            line_items_taxes = line_item['taxes']
            line_items_sku = line_item['sku']
            line_items_price = line_item['price']
            line_items_parent_name = line_item['parent_name']
            line_items_info = OrdersLineItems(order_details_id, line_items_id, line_items_name,
                                              line_items_product_id, line_items_variation_id, line_items_quantity,
                                              line_items_tax_class, line_items_subtotal, line_items_subtotal_tax,
                                              line_items_total,
                                              line_items_total_tax, line_items_sku, line_items_price,
                                              line_items_parent_name)
            db.session.add(line_items_info)
            db.session.commit()
            line_item_bc_info_complete = insertBlockChainLineItem(line_items_info)
            print(line_item_bc_info_complete)
            if int(line_item_bc_info_complete[0]) == 200:
                line_item_tx_id = line_item_bc_info_complete[1].decode("utf-8").replace("'", '"')
            else:
                line_item_tx_id = line_item_bc_info_complete[0]
            #   更新tx
            line_items_info_tx = OrdersLineItems.query.filter_by(id=line_items_info.id).one()
            if line_item_tx_id:
                line_items_info_tx.tx_id = line_item_tx_id
            db.session.commit()

            # 添加庫存
            beging_inventory, ending_inventory = getInvertoryNow(order_details_customer_id, line_items_product_id,
                                                                 line_items_quantity)
            inventory = Inventory(order_details_customer_id, beging_inventory, ending_inventory, line_items_quantity,
                                  order_details_id, line_items_product_id, 'System',
                                  'Web', '', '', '', '', '', '', '', '', '', 0)
            db.session.add(inventory)
            db.session.commit()
            inventory_bc_info = insertBlockChainInventory(inventory)
            print('inventory_create')
            print(inventory.to_json())
            print(inventory_bc_info)
            if int(inventory_bc_info[0]) == 200:
                inventory_tx_id = inventory_bc_info[1].decode("utf-8").replace("'", '"')
            else:
                inventory_tx_id = inventory_bc_info[0]
            #   更新tx
            inventory_info_tx = Inventory.query.filter_by(id=inventory.id).one()
            if inventory_tx_id:
                inventory_info_tx.tx_id = inventory_tx_id
            db.session.commit()

    # 訂單退費完成
    elif order_details_status == 'refunded':
        order_info = Orders(order_details_id, order_details_parent_id, order_details_status, billing_first_name,
                            billing_last_name, order_details_currency, order_details_version, order_details_total,
                            order_details_total_tax,
                            billing_company, billing_address_1, billing_address_2, billing_city, billing_state,
                            billing_postcode, billing_country, billing_email, billing_phone, shipping_first_name,
                            shipping_last_name, shipping_company, shipping_address_1, shipping_address_2, shipping_city,
                            shipping_state,
                            shipping_postcode, shipping_country, order_details_payment_method,
                            order_details_payment_method_title, order_details_transaction_id,
                            order_details_customer_ip_address, order_details_created_via, order_details_customer_id,
                            order_details_customer_note, order_details_cart_hash)
        db.session.add(order_info)
        db.session.commit()
        bc_order_details_Refunded = updateBlockChainOrder(order_details)
        print("Refunded")
        print(bc_order_details_Refunded)
        if int(bc_order_details_Refunded[0]) == 200:
            tx_id = bc_order_details_Refunded[1].decode("utf-8").replace("'", '"')
        else:
            tx_id = bc_order_details_Refunded[0]
        print(tx_id)
        #   更新tx
        order_info_tx = Orders.query.filter_by(id=order_info.id).one()
        if tx_id:
            order_info_tx.tx_id = tx_id
        db.session.commit()

        for line_item in line_items:
            line_items_id = line_item['id']
            line_items_name = line_item['name']
            line_items_product_id = line_item['product_id']
            line_items_variation_id = line_item['variation_id']
            line_items_quantity = line_item['quantity']
            line_items_tax_class = line_item['tax_class']
            line_items_subtotal = line_item['subtotal']
            line_items_subtotal_tax = line_item['subtotal_tax']
            line_items_total = line_item['total']
            line_items_total_tax = line_item['total_tax']
            line_items_taxes = line_item['taxes']
            line_items_sku = line_item['sku']
            line_items_price = line_item['price']
            line_items_parent_name = line_item['parent_name']
            line_items_info = OrdersLineItems(order_details_id, line_items_id, line_items_name,
                                              line_items_product_id, line_items_variation_id, line_items_quantity,
                                              line_items_tax_class, line_items_subtotal, line_items_subtotal_tax,
                                              line_items_total,
                                              line_items_total_tax, line_items_sku, line_items_price,
                                              line_items_parent_name)
            db.session.add(line_items_info)
            db.session.commit()
            line_item_bc_info_complete = insertBlockChainLineItem(line_items_info)
            print(line_item_bc_info_complete)
            if int(line_item_bc_info_complete[0]) == 200:
                line_item_tx_id = line_item_bc_info_complete[1].decode("utf-8").replace("'", '"')
            else:
                line_item_tx_id = line_item_bc_info_complete[0]
            #   更新tx
            line_items_info_tx = OrdersLineItems.query.filter_by(id=line_items_info.id).one()
            if line_item_tx_id:
                line_items_info_tx.tx_id = line_item_tx_id
            db.session.commit()

            # 庫存異動 取消時的庫存異動，須先判斷原訂單庫存是否存在
            inventory_info = Inventory.query.filter_by(user_id=order_details_customer_id,
                                                       product_id=line_items_product_id,
                                                       order_id=order_details_id).limit(1).all()
            if inventory_info:
                beging_inventory, ending_inventory = getInvertoryNow(order_details_customer_id, line_items_product_id,
                                                                     line_items_quantity * -1)
                inventory = Inventory(order_details_customer_id, beging_inventory, ending_inventory,
                                      line_items_quantity * -1,
                                      order_details_id, line_items_product_id, 'System',
                                      'Web', '', '', '', '', '', '', '', '', '', 0)
                db.session.add(inventory)
                db.session.commit()
                inventory_bc_info = insertBlockChainInventory(inventory)
                print('inventory_cancelled')
                print(inventory_bc_info)
                if int(inventory_bc_info[0]) == 200:
                    inventory_tx_id = inventory_bc_info[1].decode("utf-8").replace("'", '"')
                else:
                    inventory_tx_id = inventory_bc_info[0]
                #   更新tx
                inventory_info_tx = Inventory.query.filter_by(id=inventory.id).one()
                if inventory_tx_id:
                    inventory_info_tx.tx_id = inventory_tx_id
                db.session.commit()
    # 訂單失敗
    elif order_details_status == 'failed':
        order_info = Orders(order_details_id, order_details_parent_id, order_details_status, billing_first_name,
                            billing_last_name, order_details_currency, order_details_version, order_details_total,
                            order_details_total_tax,
                            billing_company, billing_address_1, billing_address_2, billing_city, billing_state,
                            billing_postcode, billing_country, billing_email, billing_phone, shipping_first_name,
                            shipping_last_name, shipping_company, shipping_address_1, shipping_address_2, shipping_city,
                            shipping_state,
                            shipping_postcode, shipping_country, order_details_payment_method,
                            order_details_payment_method_title, order_details_transaction_id,
                            order_details_customer_ip_address, order_details_created_via, order_details_customer_id,
                            order_details_customer_note, order_details_cart_hash)
        db.session.add(order_info)
        db.session.commit()
        bc_order_details_failed = updateBlockChainOrder(order_details)
        print("failed")
        print(bc_order_details_failed)
        if int(bc_order_details_failed[0]) == 200:
            tx_id = bc_order_details_failed[1].decode("utf-8").replace("'", '"')
        else:
            tx_id = bc_order_details_failed[0]
        print(tx_id)
        #   更新tx
        order_info_tx = Orders.query.filter_by(id=order_info.id).one()
        if tx_id:
            order_info_tx.tx_id = tx_id
        db.session.commit()

        for line_item in line_items:
            line_items_id = line_item['id']
            line_items_name = line_item['name']
            line_items_product_id = line_item['product_id']
            line_items_variation_id = line_item['variation_id']
            line_items_quantity = line_item['quantity']
            line_items_tax_class = line_item['tax_class']
            line_items_subtotal = line_item['subtotal']
            line_items_subtotal_tax = line_item['subtotal_tax']
            line_items_total = line_item['total']
            line_items_total_tax = line_item['total_tax']
            line_items_taxes = line_item['taxes']
            line_items_sku = line_item['sku']
            line_items_price = line_item['price']
            line_items_parent_name = line_item['parent_name']
            line_items_info = OrdersLineItems(order_details_id, line_items_id, line_items_name,
                                              line_items_product_id, line_items_variation_id, line_items_quantity,
                                              line_items_tax_class, line_items_subtotal, line_items_subtotal_tax,
                                              line_items_total,
                                              line_items_total_tax, line_items_sku, line_items_price,
                                              line_items_parent_name)
            db.session.add(line_items_info)
            db.session.commit()
            line_item_bc_info_complete = insertBlockChainLineItem(line_items_info)
            print(line_item_bc_info_complete)
            if int(line_item_bc_info_complete[0]) == 200:
                line_item_tx_id = line_item_bc_info_complete[1].decode("utf-8").replace("'", '"')
            else:
                line_item_tx_id = line_item_bc_info_complete[0]
            #   更新tx
            line_items_info_tx = OrdersLineItems.query.filter_by(id=line_items_info.id).one()
            if line_item_tx_id:
                line_items_info_tx.tx_id = line_item_tx_id
            db.session.commit()

    print(jsonify(order_details))
    return jsonify({
        'success': True,
        'msg': 'order record is create in blcokchain ',
        'data': order_details
    })


def bcjob():
    #查詢未上鏈的訂單
    order_infos = Orders.query.filter_by(transaction_id='404').all()
    for order_info in order_infos:
        print(order_info.id)
        bc_info = insertBlockChainOrder(order_info)
        tx_id = ''
        if int(bc_info[0]) == 200:
            tx_id = bc_info[1].decode("utf-8").replace("'", '"')
        else:
            tx_id = bc_info[0]
        print(tx_id)
        #   更新tx
        order_info_tx = Orders.query.filter_by(id=order_info.id).one()
        if tx_id:
            order_info_tx.tx_id = tx_id
        db.session.commit()

@app.route('/pcs/api/v1/bc/cancel', methods=['POST'])
def ordercancel():
    request_data = request.data.decode('utf-8')
    if not request_data:
        return jsonify({
            'success': False
        })

    # 本機測試時請打開
    # j_request_data = json.loads(request_data)
    # req_id = j_request_data['id']
    # orderid = 'orders/' + str(req_id)
    # # 無jwt調用方式
    # # order_details = wcapi.get(orderid).json()
    # r = requests.post(end_point_url_posts, data=payload)
    # jwt_info = r.content.decode("utf-8").replace("'", '"')
    # data = json.loads(jwt_info)
    # my_headers = {'Authorization': "Bearer " + data['token']}
    # res_order_details = requests.get('https://store.pyrarc.com/wp-json/wc/v3/orders/' + str(req_id), data=payload,
    #                                  headers=my_headers)
    # order_details = json.loads(res_order_details.content.decode("utf-8").replace("'", '"'))

    # 正式環境webhook可以直接獲取到
    order_details = json.loads(request_data)
    order_details_id = order_details['id']
    order_details_parent_id = order_details['parent_id']
    order_details_status = order_details['status']
    order_details_currency = order_details['currency']
    order_details_version = order_details['version']
    order_details_date_created = order_details['date_created']
    order_details_date_modified = order_details['date_modified']
    order_details_total = order_details['total']
    order_details_total_tax = order_details['total_tax']
    order_details_payment_method = order_details['payment_method']
    order_details_payment_method_title = order_details['payment_method_title']
    order_details_transaction_id = order_details['transaction_id']
    order_details_customer_ip_address = order_details['customer_ip_address']
    order_details_created_via = order_details['created_via']
    order_details_customer_id = order_details['customer_id']
    order_details_customer_note = order_details['customer_note']
    order_details_cart_hash = order_details['cart_hash']

    # 保存billing訊息
    billing = order_details['billing']
    billing_first_name = billing['first_name']
    billing_last_name = billing['last_name']
    billing_company = billing['company']
    billing_address_1 = billing['address_1']
    billing_address_2 = billing['address_2']
    billing_city = billing['city']
    billing_state = billing['state']
    billing_postcode = billing['postcode']
    billing_country = billing['country']
    billing_email = billing['email']
    billing_phone = billing['phone']
    # 保存shipping訊息
    shipping = order_details['shipping']
    shipping_first_name = shipping['first_name']
    shipping_last_name = shipping['last_name']
    shipping_company = shipping['company']
    shipping_address_1 = shipping['address_1']
    shipping_address_2 = shipping['address_2']
    shipping_city = shipping['city']
    shipping_state = shipping['state']
    shipping_postcode = shipping['postcode']
    shipping_country = shipping['country']
    # 保存line items
    line_items = order_details['line_items']
    # line_items_id = line_items['id']
    # line_items_name = line_items['name']
    # line_items_product_id = line_items['product_id']
    # line_items_variation_id = line_items['variation_id']
    # line_items_quantity = line_items['quantity']
    # line_items_tax_class = line_items['tax_class']
    # line_items_subtotal = line_items['subtotal']
    # line_items_subtotal_tax = line_items['subtotal_tax']
    # line_items_total = line_items['total']
    # line_items_total_tax = line_items['total_tax']
    # line_items_taxes = line_items['taxes']
    # line_items_sku = line_items['sku']
    # line_items_price = line_items['price']
    # line_items_parent_name = line_items['parent_name']

    # 保存資料庫
    order_info = Orders(order_details_id, order_details_parent_id, order_details_status, billing_first_name,
                        billing_last_name, order_details_currency, order_details_version, order_details_total,
                        order_details_total_tax,
                        billing_company, billing_address_1, billing_address_2, billing_city, billing_state,
                        billing_postcode, billing_country, billing_email, billing_phone, shipping_first_name,
                        shipping_last_name, shipping_company, shipping_address_1, shipping_address_2, shipping_city,
                        shipping_state,
                        shipping_postcode, shipping_country, order_details_payment_method,
                        order_details_payment_method_title, order_details_transaction_id,
                        order_details_customer_ip_address, order_details_created_via, order_details_customer_id,
                        order_details_customer_note, order_details_cart_hash)
    db.session.add(order_info)
    db.session.commit()
    # 保存資料庫

    for line_item in line_items:
        line_items_id = line_item['id']
        line_items_name = line_item['name']
        line_items_product_id = line_item['product_id']
        line_items_variation_id = line_item['variation_id']
        line_items_quantity = line_item['quantity']
        line_items_tax_class = line_item['tax_class']
        line_items_subtotal = line_item['subtotal']
        line_items_subtotal_tax = line_item['subtotal_tax']
        line_items_total = line_item['total']
        line_items_total_tax = line_item['total_tax']
        line_items_taxes = line_item['taxes']
        line_items_sku = line_item['sku']
        line_items_price = line_item['price']
        line_items_parent_name = line_item['parent_name']
        line_items_info = OrdersLineItems(order_details_id, line_items_id, line_items_name,
                                          line_items_product_id, line_items_variation_id, line_items_quantity,
                                          line_items_tax_class, line_items_subtotal, line_items_subtotal_tax,
                                          line_items_total,
                                          line_items_total_tax, line_items_sku, line_items_price,
                                          line_items_parent_name)
        db.session.add(line_items_info)
        db.session.commit()

    print(jsonify(order_details))
    return jsonify({
        'success': True,
        'msg': 'order record is create in blcokchain ',
        'data': order_details
    })


@app.route('/pcs/api/v1/invoice', methods=['POST'])
def invoice_details():
    request_data = request.data.decode('utf-8')
    if not request_data:
        return jsonify({
            'success': False
        })
    data = json.loads(request_data)
    order_details = getOrderDetail(data['order_id'])
    if not order_details:
        return jsonify({
            'success': False,
            'msg': ' order is not exist'
        })
    order_info = Orders.query.filter_by(order_id=order_details['id'], state='pending').first()
    if not order_info:
        return jsonify({
            'success': False,
            'msg': ' order is not exist in pcs'
        })
    CarruerType = int(data['CarruerType'])
    # 綠界科技電子發票載具
    if CarruerType == 1:
        CarruerNum = '50873438' + str(order_details['customer_id'])
        (CarruerType, CarruerNum)
        order_info.carruer_num = CarruerNum
    # 自然人憑證
    elif CarruerType == 2:
        CarruerNum = data['CarruerNum']
        (CarruerType, CarruerNum)
        order_info.carruer_num = CarruerNum
    # 手機條碼
    elif CarruerType == 3:
        CarruerNum = data['CarruerNum']
        (CarruerType, CarruerNum)
        order_info.carruer_num = CarruerNum
    # 公司統編
    elif CarruerType == 4:
        CustomerIdentifier = data['CustomerIdentifier']
        (CarruerType, CustomerIdentifier)
        order_info.customer_identifier = CustomerIdentifier
    # 捐贈碼
    elif CarruerType == 5:
        LoveCode = data['LoveCode']
        (CarruerType, LoveCode)
        order_info.lovecode = LoveCode
    else:
        return jsonify({
            'success': False,
            'msg': ' CarruerType is not exist'
        })
    order_info.carruer_type = CarruerType
    db.session.commit()

    return jsonify({
        'success': True,
        'msg': ' invoice info is add'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
