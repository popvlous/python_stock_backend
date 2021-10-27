import json

import requests
from flask import jsonify, app, request
from sqlalchemy import desc, func, and_

from model import Orders, Inventory, db, Delivery
from util import insertBlockChainDelivery, insertBlockChainInventory

user_name = "pyrarc.app"
user_passwd = "B8I%7s2MnQ1&nTM9OYP15ms0"
end_point_url_posts = "https://store.pyrarc.com/wp-json/jwt-auth/v1/token"

payload = {
    "username": user_name,
    "password": user_passwd
}


def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code


# 獲取最新庫存
def getEndInvertory(user_id=None, product_id=None):
    invertory_info = Inventory.query.filter_by(user_id=user_id, product_id=product_id).order_by(
        desc(Inventory.id)).limit(
        1).all()
    if invertory_info:
        return invertory_info[0].ending_inventory
    else:
        return


# 獲取最新庫存
def getInvertoryNow(user_id=None, product_id=None, adj_amount=None):
    invertory_info = Inventory.query.filter_by(user_id=user_id, product_id=product_id).order_by(
        desc(Inventory.id)).limit(
        1).all()
    if invertory_info:
        beging_inventory = invertory_info[0].ending_inventory
        ending_inventory = beging_inventory + adj_amount
    else:
        beging_inventory = 0
        ending_inventory = adj_amount
    return beging_inventory, ending_inventory


# 查詢最新庫存by客戶ＩＤ跟產品號碼
def inventory(customer_id: int):
    # inventories = Inventory.query.filter_by(user_id=customer_id, product_id=product_id).order_by(desc(Inventory.id)).limit(1).all()
    # inventories = db.session.query(func.max(Inventory.id), Inventory.user_id, Inventory.product_id,Inventory.ending_inventory).filter_by(user_id=customer_id).group_by(Inventory.id,Inventory.user_id,Inventory.product_id,Inventory.ending_inventory).all()
    subq = db.session.query(Inventory.user_id, Inventory.product_id, func.max(Inventory.id).label('max_id')).group_by(
        Inventory.user_id, Inventory.product_id).subquery('t2')

    inventories = db.session.query(Inventory).filter_by(user_id=customer_id).join(subq, and_(
        Inventory.user_id == subq.c.user_id, Inventory.id == subq.c.max_id)).all()

    r = requests.post(end_point_url_posts, data=payload)
    jwt_info = r.content.decode("utf-8").replace("'", '"')
    data = json.loads(jwt_info)
    s = json.dumps(data, indent=4, sort_keys=True)
    print(s)
    token = data['token']
    Auth_token = "Bearer " + token

    my_headers = {'Authorization': Auth_token}

    if inventories:
        # productlist = wcapi.get("products", params={"per_page": 20}).json()
        for inv in inventories:
            response_productlist = requests.get(
                'https://store.pyrarc.com/wp-json/wc/v3/products/' + str(inv.product_id), data=payload,
                headers=my_headers)
            productlist = json.loads(response_productlist.content.decode("utf-8").replace("'", '"'))
            inv.product_name = productlist["name"]
        # inventory = inventories[0]
        return jsonify([inventory.to_json_ext() for inventory in inventories])
    else:
        return jsonify({
            'message': 'data is not exist'
        })


# 新增庫存
def inventoryadd():
    req = request.data.decode("utf-8").replace("'", '"')
    data = json.loads(req)
    user_id = data['user_id']
    adj_amount = data['adj_amount']
    order_id = data['order_id']
    product_id = data['product_id']
    create_by = data['create_by']
    order_source = data['order_source']
    # 獲取最新的庫存
    beging_inventory, ending_inventory = getInvertoryNow(user_id, product_id, adj_amount)
    inventory = Inventory(user_id, beging_inventory, ending_inventory, adj_amount, order_id, product_id, create_by,
                          order_source, '', '', '', '', '', '', '', '', '', 0)
    db.session.add(inventory)
    db.session.commit()
    return jsonify({
        'success': True,
        'msg': 'inventory is added now ',
        'data': data
    })


# # 指配派送
# def inventorydelivery():
#     req = request.data.decode("utf-8").replace("'", '"')
#     data = json.loads(req)
#     user_id = data['user_id']
#     adj_amount = data['adj_amount']
#     product_id = data['product_id']
#     create_by = data['create_by']
#     order_source = data['order_source']
#     shipping_first_name = data['shipping_first_name']
#     shipping_last_name = data['shipping_last_name']
#     shipping_company = data['shipping_company']
#     shipping_address_1 = data['shipping_address_1']
#     shipping_city = data['shipping_city']
#     shipping_postcode = data['shipping_postcode']
#     shipping_country = data['shipping_country']
#     shipping_phone = data['shipping_phone']
#     remark = data['remark']
#     # 判斷配送的數量是否超過現有庫存
#     Inventory_now = getEndInvertory(user_id, product_id)
#     if Inventory_now < adj_amount * -1:
#         return jsonify({
#             'message': 'Quantities is not enough'
#         })
#     # 獲取最新的庫存
#     beging_inventory, ending_inventory = getInvertoryNow(user_id, product_id, adj_amount)
#     inventory = Inventory(user_id, beging_inventory, ending_inventory, adj_amount, 0, product_id, create_by,
#                           order_source, shipping_first_name, shipping_last_name, shipping_company, shipping_address_1,
#                           shipping_city, shipping_postcode, shipping_country, shipping_phone, remark)
#     db.session.add(inventory)
#     db.session.commit()
#     return jsonify({
#         'success': True,
#         'msg': 'inventory is added now ',
#         'data': data
#     })


# 單一物件指派

def inventorydelivery():
    req = request.data.decode("utf-8").replace("'", '"')
    data = json.loads(req)
    user_id = data['user_id']
    adj_amount = data['adj_amount']
    product_id = data['product_id']
    create_by = data['create_by']
    order_source = data['order_source']
    shipping_first_name = data['shipping_first_name']
    shipping_last_name = data['shipping_last_name']
    shipping_company = data['shipping_company']
    shipping_address_1 = data['shipping_address_1']
    shipping_city = data['shipping_city']
    shipping_state = data['shipping_state']
    shipping_postcode = data['shipping_postcode']
    shipping_country = data['shipping_country']
    shipping_phone = data['shipping_phone']
    remark = data['remark']
    # 判斷配送的數量是否超過現有庫存
    Inventory_now = getEndInvertory(user_id, product_id)
    if Inventory_now < adj_amount * -1:
        return jsonify({
            'message': 'Quantities is not enough'
        })
    # 產生配送單
    delivery = Delivery(user_id, create_by, order_source, shipping_first_name, shipping_last_name, shipping_company,
                        shipping_address_1, shipping_city, shipping_state,shipping_postcode, shipping_country,
                        shipping_phone)
    db.session.add(delivery)
    db.session.commit()
    # 獲取最新的庫存
    beging_inventory, ending_inventory = getInvertoryNow(user_id, product_id, adj_amount)
    inventory = Inventory(user_id, beging_inventory, ending_inventory, adj_amount, 0, product_id, create_by,
                          order_source, shipping_first_name, shipping_last_name, shipping_company, shipping_address_1,
                          shipping_city, shipping_postcode, shipping_country, shipping_phone, remark, delivery.id)
    db.session.add(inventory)
    db.session.commit()
    token = 'M5g5yVHMV2gc6iRvs1xu5Bsb9OEj0Wux8pQcKknldMo'
    msg = '用戶已指派寄送，請登入平台，輸入物流單號 https://storeapi.pyrarc.com/backend/inventorylist?mid=' + str(inventory.id)
    lineNotifyMessage(token, msg)
    return jsonify({
        'success': True,
        'msg': 'inventory is added now ',
        'data': data
    })


# 多物件指派

def inventorydeliveries():
    req = request.data.decode("utf-8").replace("'", '"')
    data = json.loads(req)
    #正式環境請開通由form來
    #data = request.form
    user_id = data['user_id']
    adj_amount_set = data['adj_amount']
    create_by = data['create_by']
    order_source = data['order_source']
    shipping_first_name = data['shipping_first_name']
    shipping_last_name = data['shipping_last_name']
    shipping_company = data['shipping_company']
    shipping_address_1 = data['shipping_address_1']
    shipping_city = data['shipping_city']
    shipping_state = data['shipping_state']
    shipping_postcode = data['shipping_postcode']
    shipping_country = data['shipping_country']
    shipping_phone = data['shipping_phone']
    remark = data['remark']

    #先檢查庫存是否夠
    adj_amount_infos = adj_amount_set.split(';')
    for adj_amount_info in adj_amount_infos:
        if adj_amount_info:
            adj_amount_detial = adj_amount_info.split(',')
            product_id = int(adj_amount_detial[0])
            adj_amount = int(adj_amount_detial[2])
            Inventory_now = getEndInvertory(user_id, product_id)
            if Inventory_now is not None:
                if Inventory_now < adj_amount:
                    return jsonify({
                        'success': 'false',
                        'msg': str(product_id) + ' Quantities is not enough'
                    })
            else:
                return jsonify({
                    'success': 'false',
                    'msg': 'Quantities is not exist'
                })

    # 產生配送單
    delivery = Delivery(user_id, create_by, order_source, shipping_first_name, shipping_last_name, shipping_company,
                        shipping_address_1, shipping_city, shipping_state, shipping_postcode, shipping_country,
                        shipping_phone)
    db.session.add(delivery)
    db.session.commit()
    # 配送單上鏈
    delivery_bc_info = insertBlockChainDelivery(delivery)
    print(delivery_bc_info)
    if int(delivery_bc_info[0]) == 200:
        delivery_tx_id = delivery_bc_info[1].decode("utf-8").replace("'", '"')
    else:
        delivery_tx_id = delivery_bc_info[0]
    #   更新tx
    delivery_info_tx = Delivery.query.filter_by(id=delivery.id).one()
    if delivery_tx_id:
        delivery_info_tx.tx_id = delivery_tx_id
    db.session.commit()

    # 獲取最新的庫存
    for adj_amount_info in adj_amount_infos:
        if adj_amount_info:
            adj_amount_detial = adj_amount_info.split(',')
            product_id = int(adj_amount_detial[0])
            adj_amount = int(adj_amount_detial[2])
            #多物件指派時，扣除數量需修正為負數
            beging_inventory, ending_inventory = getInvertoryNow(user_id, product_id, adj_amount * -1)
            inventory = Inventory(user_id, beging_inventory, ending_inventory, adj_amount * -1, 0, product_id, create_by,
                                  order_source, shipping_first_name, shipping_last_name, shipping_company,
                                  shipping_address_1,
                                  shipping_city, shipping_postcode, shipping_country, shipping_phone, remark, delivery.id)
            db.session.add(inventory)
            db.session.commit()
            #庫存上鏈
            inventory_bc_info = insertBlockChainInventory(inventory)
            print('inventory_discount:'+str(product_id))
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

    # line通知
    token = 'M5g5yVHMV2gc6iRvs1xu5Bsb9OEj0Wux8pQcKknldMo'
    msg = '用戶已指派寄送，請登入平台，輸入物流單號 https://storeapi.pyrarc.com/backend/deliverylist?mid=' + str(delivery.id)
    lineNotifyMessage(token, msg)
    return jsonify({
        'success': 'true',
        'msg': 'delivery is added now '
    })


# 獲取五筆庫存紀錄
def inventoryhistory(customer_id: int):
    inventories = Inventory.query.filter_by(user_id=customer_id, order_id=0).order_by(desc(Inventory.id)).limit(5).all()
    if inventories:
        for inv in inventories:
            inv.adj_amount = int(inv.adj_amount) * -1
        return jsonify([inventory.to_json() for inventory in inventories])
    else:
        return jsonify({
            'message': 'data is not exist!!'
        })


# 獲取五筆指派紀錄
def deliveryhistory(customer_id: int):
    # inventories =  db.session.query(func.sum(Inventory.ending_inventory), Inventory.user_id, Inventory.product_id).filter_by(user_id=customer_id).group_by(Inventory.user_id,Inventory.product_id).all()
    subq = db.session.query(Inventory.user_id, Inventory.product_id, Inventory.delivery_id, Inventory.ending_inventory, Inventory.adj_amount, func.max(Inventory.id).label('max_id')).group_by(Inventory.user_id, Inventory.product_id, Inventory.delivery_id, Inventory.ending_inventory, Inventory.adj_amount).subquery('t2')

    deliveries = db.session.query(Delivery.id, Delivery.user_id, func.sum(subq.c.ending_inventory), func.sum(subq.c.adj_amount), Delivery.create_time,
                                  Delivery.modify_time, Delivery.create_by, Delivery.order_source, Delivery.location,
                                  Delivery.shipping_first_name, Delivery.shipping_last_name, Delivery.shipping_company,
                                  Delivery.shipping_address_1, Delivery.shipping_city, Delivery.shipping_state, Delivery.shipping_postcode,
                                  Delivery.shipping_country, Delivery.shipping_phone,
                                  Delivery.shipment_number, Delivery.tx_id).filter_by(user_id=customer_id).join(subq, and_(
        Delivery.user_id == subq.c.user_id, Delivery.id == subq.c.delivery_id)).group_by(Delivery.user_id,
                                                                                         Delivery.id).order_by(desc(Delivery.id)).limit(5).all()

    delivery_infos = []

    if deliveries:
        for delivery in deliveries:
            delivery_info = {
                'id': delivery.id,
                'user_id': delivery.user_id,
                'ending_inventory': str(delivery[2]),
                'total_adj_amount': int(delivery[3]) * -1,
                'create_time': delivery.create_time,
                'modify_time': delivery.modify_time,
                'create_by': delivery.create_by,
                'order_source': delivery.order_source,
                'shipping_first_name': delivery.shipping_first_name,
                'shipping_last_name': delivery.shipping_last_name,
                'shipping_company': delivery.shipping_company,
                'shipping_address_1': delivery.shipping_address_1,
                'shipping_city': delivery.shipping_city,
                'shipping_state': delivery.shipping_state,
                'shipping_postcode': delivery.shipping_postcode,
                'shipping_country': delivery.shipping_country,
                'shipping_phone': delivery.shipping_phone,
                'shipment_number': delivery.shipment_number,
                'tx_id':delivery.tx_id
            }
            delivery_infos.append(delivery_info)
        return jsonify([info for info in delivery_infos])
    else:
        return jsonify({
            'message': 'data is not exist'
        })
