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


class Orders(db.Model):
    __table__name = 'orders'
    # 設定 primary_key
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)
    state = db.Column(db.String(50), nullable=True)
    billing_first_name = db.Column(db.String(50), nullable=True)
    billing_last_name = db.Column(db.String(50), nullable=True)
    date_created = db.Column(db.DateTime, nullable=True)
    date_modified = db.Column(db.DateTime, nullable=True)
    total = db.Column(db.Integer, nullable=True)
    total_tax = db.Column(db.Integer, nullable=True)
    currency = db.Column(db.String(11), nullable=True)
    version = db.Column(db.String(11), nullable=True)
    customer_id = db.Column(db.Integer)
    order_key = db.Column(db.String(100), nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    payment_method_title = db.Column(db.String(50), nullable=True)
    transaction_id = db.Column(db.String(50), nullable=True)
    customer_ip_address = db.Column(db.String(50), nullable=True)
    created_via = db.Column(db.String(50), nullable=True)
    customer_id = db.Column(db.Integer, nullable=True)
    customer_note = db.Column(db.String(50), nullable=True)
    date_completed = db.Column(db.String(50), nullable=True)
    date_paid = db.Column(db.String(50), nullable=True)
    cart_hash = db.Column(db.String(50), nullable=True)
    billing_company = db.Column(db.String(50), nullable=True)
    billing_address_1 = db.Column(db.String(500), nullable=True)
    billing_address_2 = db.Column(db.String(500), nullable=True)
    billing_city = db.Column(db.String(50), nullable=True)
    billing_state = db.Column(db.String(50), nullable=True)
    billing_postcode = db.Column(db.String(50), nullable=True)
    billing_country = db.Column(db.String(50), nullable=True)
    billing_email = db.Column(db.String(50), nullable=True)
    billing_phone = db.Column(db.String(50), nullable=True)
    shipping_first_name = db.Column(db.String(50), nullable=True)
    shipping_last_name = db.Column(db.String(50), nullable=True)
    shipping_company = db.Column(db.String(50), nullable=True)
    shipping_address_1 = db.Column(db.String(500), nullable=True)
    shipping_address_2 = db.Column(db.String(500), nullable=True)
    shipping_city = db.Column(db.String(50), nullable=True)
    shipping_state = db.Column(db.String(50), nullable=True)
    shipping_postcode = db.Column(db.String(50), nullable=True)
    shipping_country = db.Column(db.String(50), nullable=True)
    tx_id = db.Column(db.String(200), nullable=True)
    customer_identifier = db.Column(db.Integer)
    carruer_type = db.Column(db.Integer)
    carruer_num = db.Column(db.String(100), nullable=True)
    lovecode = db.Column(db.String(100), nullable=True)

    def __init__(self, order_id, parent_id, state, billing_first_name, billing_last_name, currency, version, total,
                 total_tax, billing_company, billing_address_1, billing_address_2, billing_city, billing_state,
                 billing_postcode, billing_country, billing_email, billing_phone, shipping_first_name,
                 shipping_last_name, shipping_company, shipping_address_1, shipping_address_2, shipping_city,
                 shipping_state,
                 shipping_postcode, shipping_country, payment_method, payment_method_title, transaction_id,
                 customer_ip_address, created_via, customer_id, customer_note, cart_hash):
        self.order_id = order_id
        self.parent_id = parent_id
        self.state = state
        self.billing_first_name = billing_first_name
        self.billing_last_name = billing_last_name
        self.currency = currency
        self.version = version
        self.total = total
        self.total_tax = total_tax
        self.date_created = datetime.utcnow()
        self.date_modified = datetime.utcnow()
        self.billing_company = billing_company
        self.billing_address_1 = billing_address_1
        self.billing_address_2 = billing_address_2
        self.billing_city = billing_city
        self.billing_state = billing_state
        self.billing_postcode = billing_postcode
        self.billing_country = billing_country
        self.billing_email = billing_email
        self.billing_phone = billing_phone
        self.shipping_first_name = shipping_first_name
        self.shipping_last_name = shipping_last_name
        self.shipping_company = shipping_company
        self.shipping_address_1 = shipping_address_1
        self.shipping_address_2 = shipping_address_2
        self.shipping_city = shipping_city
        self.shipping_state = shipping_state
        self.shipping_postcode = shipping_postcode
        self.shipping_country = shipping_country
        self.payment_method = payment_method
        self.payment_method_title = payment_method_title
        self.transaction_id = transaction_id
        self.customer_ip_address = customer_ip_address
        self.created_via = created_via
        self.customer_id = customer_id
        self.customer_note = customer_note
        self.cart_hash = cart_hash

    def to_json(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'parent_id': self.parent_id,
            'state': self.state,
            'billing_first_name': self.billing_first_name,
            'billing_last_name': self.billing_last_name,
            'currency': self.currency,
            'version': self.version,
            'total': self.total,
            'total_tax': self.total_tax,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'billing_company': self.billing_company,
            'billing_address_1': self.billing_address_1,
            'billing_address_2': self.billing_address_2,
            'billing_city': self.billing_city,
            'billing_state': self.billing_state,
            'billing_postcode': self.billing_postcode,
            'billing_country': self.billing_country,
            'billing_email': self.billing_email,
            'billing_phone': self.billing_phone,
            'shipping_first_name': self.shipping_first_name,
            'shipping_last_name': self.shipping_last_name,
            'shipping_company': self.shipping_company,
            'shipping_address_1': self.shipping_address_1,
            'shipping_address_2': self.shipping_address_2,
            'shipping_city': self.shipping_city,
            'shipping_state': self.shipping_state,
            'shipping_postcode': self.shipping_postcode,
            'shipping_country': self.shipping_country,
            'payment_method': self.payment_method,
            'payment_method_title': self.payment_method_title,
            'transaction_id': self.transaction_id,
            'customer_ip_address': self.customer_ip_address,
            'created_via': self.created_via,
            'customer_id': self.customer_id,
            'customer_note': self.customer_note,
            'cart_hash': self.cart_hash,
            'tx_id': self.tx_id
        }

    def to_json_ext(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'parent_id': self.parent_id,
            'state': self.state,
            'billing_first_name': self.billing_first_name,
            'billing_last_name': self.billing_last_name,
            'currency': self.currency,
            'version': self.version,
            'total': self.total,
            'total_tax': self.total_tax,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'billing_company': self.billing_company,
            'billing_address_1': self.billing_address_1,
            'billing_address_2': self.billing_address_2,
            'billing_city': self.billing_city,
            'billing_state': self.billing_state,
            'billing_postcode': self.billing_postcode,
            'billing_country': self.billing_country,
            'billing_email': self.billing_email,
            'billing_phone': self.billing_phone,
            'shipping_first_name': self.shipping_first_name,
            'shipping_last_name': self.shipping_last_name,
            'shipping_company': self.shipping_company,
            'shipping_address_1': self.shipping_address_1,
            'shipping_address_2': self.shipping_address_2,
            'shipping_city': self.shipping_city,
            'shipping_state': self.shipping_state,
            'shipping_postcode': self.shipping_postcode,
            'shipping_country': self.shipping_country,
            'payment_method': self.payment_method,
            'payment_method_title': self.payment_method_title,
            'transaction_id': self.transaction_id,
            'customer_ip_address': self.customer_ip_address,
            'created_via': self.created_via,
            'customer_id': self.customer_id,
            'customer_note': self.customer_note,
            'cart_hash': self.cart_hash,
            'checkinfo': self.checkinfo,
            'tx_id': self.tx_id
        }


class OrdersLineItems(db.Model):
    __table__name = 'orders_line_items'
    # 設定 primary_key
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    line_items_id = db.Column(db.Integer)
    line_items_name = db.Column(db.String(100), nullable=True)
    line_items_product_id = db.Column(db.Integer)
    line_items_variation_id = db.Column(db.Integer)
    line_items_quantity = db.Column(db.Integer)
    line_items_tax_class = db.Column(db.String(100), nullable=True)
    line_items_subtotal = db.Column(db.Numeric(10, 6))
    line_items_subtotal_tax = db.Column(db.Numeric(10, 6))
    line_items_total = db.Column(db.Numeric(10, 6))
    line_items_total_tax = db.Column(db.Numeric(10, 6))
    line_items_taxes = db.Column(db.String(100), nullable=True)
    line_items_sku = db.Column(db.String(50), nullable=True)
    line_items_price = db.Column(db.Numeric(10, 6))
    line_items_parent_name = db.Column(db.String(100), nullable=True)
    tx_id = db.Column(db.String(100), nullable=True)

    def __init__(self, order_id, line_items_id, line_items_name, line_items_product_id,
                 line_items_variation_id, line_items_quantity, line_items_tax_class, line_items_subtotal,
                 line_items_subtotal_tax, line_items_total, line_items_total_tax, line_items_sku, line_items_price,
                 line_items_parent_name):
        self.order_id = order_id
        self.line_items_id = line_items_id
        self.line_items_name = line_items_name
        self.line_items_product_id = line_items_product_id
        self.line_items_variation_id = line_items_variation_id
        self.line_items_quantity = line_items_quantity
        self.line_items_tax_class = line_items_tax_class
        self.line_items_subtotal = line_items_subtotal
        self.line_items_subtotal_tax = line_items_subtotal_tax
        self.line_items_total = line_items_total
        self.line_items_total_tax = line_items_total_tax
        # self.line_items_taxes = line_items_taxes
        self.line_items_sku = line_items_sku
        self.line_items_price = line_items_price
        self.line_items_parent_name = line_items_parent_name


def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)


class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    beging_inventory = db.Column(db.Integer)
    ending_inventory = db.Column(db.Integer)
    adj_amount = db.Column(db.String(50))
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    modify_time = db.Column(db.DateTime, index=True, default=datetime.now)
    transaction_id = db.Column(db.String(100))
    order_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    create_by = db.Column(db.String(100))
    order_source = db.Column(db.String(100))
    location = db.Column(db.String(100))
    shipping_first_name = db.Column(db.String(50), nullable=True)
    shipping_last_name = db.Column(db.String(50), nullable=True)
    shipping_company = db.Column(db.String(50), nullable=True)
    shipping_address_1 = db.Column(db.String(500), nullable=True)
    shipping_address_2 = db.Column(db.String(500), nullable=True)
    shipping_city = db.Column(db.String(50), nullable=True)
    shipping_postcode = db.Column(db.String(50), nullable=True)
    shipping_country = db.Column(db.String(50), nullable=True)
    shipping_phone = db.Column(db.String(50), nullable=True)
    shipment_number = db.Column(db.String(50), nullable=True)
    delivery_id = db.Column(db.Integer)
    remark = db.Column(db.String(50))
    tx_id = db.Column(db.String(200), nullable=True)

    def __init__(self, user_id, beging_inventory, ending_inventory, adj_amount, order_id, product_id, create_by,
                 order_source, shipping_first_name, shipping_last_name, shipping_company, shipping_address_1,
                 shipping_city, shipping_postcode, shipping_country, shipping_phone, remark, delivery_id):
        self.user_id = user_id
        self.beging_inventory = beging_inventory
        self.ending_inventory = ending_inventory
        self.adj_amount = adj_amount
        self.order_id = order_id
        self.product_id = product_id
        self.create_by = create_by
        self.order_source = order_source
        self.create_time = datetime.utcnow()
        self.modify_time = datetime.utcnow()
        self.shipping_first_name = shipping_first_name
        self.shipping_last_name = shipping_last_name
        self.shipping_company = shipping_company
        self.shipping_address_1 = shipping_address_1
        self.shipping_city = shipping_city
        self.shipping_postcode = shipping_postcode
        self.shipping_country = shipping_country
        self.shipping_phone = shipping_phone
        self.remark = remark
        self.delivery_id = delivery_id

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'beging_inventory': self.beging_inventory,
            'ending_Inventory': self.ending_inventory,
            'adj_amount': self.adj_amount,
            'create_time': self.create_time,
            'modify_time': self.modify_time,
            'transaction_id': self.transaction_id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'create_by': self.create_by,
            'order_source': self.order_source,
            'shipping_first_name': self.shipping_first_name,
            'shipping_last_name': self.shipping_last_name,
            'shipping_company': self.shipping_company,
            'shipping_address_1': self.shipping_address_1,
            'shipping_address_2': self.shipping_address_2,
            'shipping_city': self.shipping_city,
            'shipping_postcode': self.shipping_postcode,
            'shipping_country': self.shipping_country,
            'shipping_phone': self.shipping_phone,
            'shipment_number': self.shipment_number,
            'delivery_id': self.delivery_id,
            'remark': self.remark,
            'tx_id': self.tx_id
        }

    def to_json_ext(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'beging_inventory': self.beging_inventory,
            'ending_Inventory': self.ending_inventory,
            'adj_amount': self.adj_amount,
            'create_time': self.create_time,
            'modify_time': self.modify_time,
            'transaction_id': self.transaction_id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'create_by': self.create_by,
            'order_source': self.order_source,
            'shipping_first_name': self.shipping_first_name,
            'shipping_last_name': self.shipping_last_name,
            'shipping_company': self.shipping_company,
            'shipping_address_1': self.shipping_address_1,
            'shipping_address_2': self.shipping_address_2,
            'shipping_city': self.shipping_city,
            'shipping_postcode': self.shipping_postcode,
            'shipping_country': self.shipping_country,
            'shipping_phone': self.shipping_phone,
            'shipment_number': self.shipment_number,
            'delivery_id': self.delivery_id,
            'remark': self.remark,
            'tx_id': self.tx_id
        }


class InventoryMeta(db.Model):
    __tablename__ = 'inventorymeta'
    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer)
    purchase_type = db.Column(db.Integer)
    vaild_time = db.Column(db.DateTime, index=True, default=datetime.now)
    remark = db.Column(db.String(50))

    def __init__(self, role_name, role_status):
        self.role_name = role_name
        self.role_status = role_status
        self.base_create_time = datetime.utcnow()
        self.base_modify_time = datetime.utcnow()


class Delivery(db.Model):
    __tablename__ = 'delivery'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    modify_time = db.Column(db.DateTime, index=True, default=datetime.now)
    create_by = db.Column(db.String(100))
    order_source = db.Column(db.String(100))
    location = db.Column(db.String(100))
    shipping_first_name = db.Column(db.String(50), nullable=True)
    shipping_last_name = db.Column(db.String(50), nullable=True)
    shipping_company = db.Column(db.String(50), nullable=True)
    shipping_address_1 = db.Column(db.String(500), nullable=True)
    shipping_address_2 = db.Column(db.String(500), nullable=True)
    shipping_city = db.Column(db.String(50), nullable=True)
    shipping_state = db.Column(db.String(50), nullable=True)
    shipping_postcode = db.Column(db.String(50), nullable=True)
    shipping_country = db.Column(db.String(50), nullable=True)
    shipping_phone = db.Column(db.String(50), nullable=True)
    shipment_number = db.Column(db.String(50), nullable=True)
    remark = db.Column(db.String(50))
    tx_id = db.Column(db.String(200), nullable=True)

    def __init__(self, user_id, create_by, order_source, shipping_first_name, shipping_last_name, shipping_company,
                 shipping_address_1, shipping_city, shipping_state, shipping_postcode, shipping_country,
                 shipping_phone):
        self.user_id = user_id
        self.create_by = create_by
        self.order_source = order_source
        self.create_time = datetime.utcnow()
        self.modify_time = datetime.utcnow()
        self.shipping_first_name = shipping_first_name
        self.shipping_last_name = shipping_last_name
        self.shipping_company = shipping_company
        self.shipping_address_1 = shipping_address_1
        self.shipping_city = shipping_city
        self.shipping_state = shipping_state
        self.shipping_postcode = shipping_postcode
        self.shipping_country = shipping_country
        self.shipping_phone = shipping_phone

    def to_json(self):
        return {
            'id': self.id,
            'create_time': self.create_time,
            'modify_time': self.modify_time,
            'create_by': self.create_by,
            'order_source': self.order_source,
            'shipping_first_name': self.shipping_first_name,
            'shipping_last_name': self.shipping_last_name,
            'shipping_company': self.shipping_company,
            'shipping_address_1': self.shipping_address_1,
            'shipping_city': self.shipping_city,
            'shipping_state': self.shipping_state,
            'shipping_postcode': self.shipping_postcode,
            'shipping_country': self.shipping_country,
            'shipping_phone': self.shipping_phone,
            'shipment_number': self.shipment_number,
            'remark': self.remark,
            'tx_id': self.tx_id
        }
