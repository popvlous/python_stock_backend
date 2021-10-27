import json
from datetime import datetime

import aiohttp
import requests
from flask import app

from model import Orders

token = "SEY3QW9ES2ZBbw=="

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
}

user_name = "pyrarc.app"
user_passwd = "B8I%7s2MnQ1&nTM9OYP15ms0"
end_point_url_posts = "https://store.pyrarc.com/wp-json/jwt-auth/v1/token"

payload = {
    "username": user_name,
    "password": user_passwd
}


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def insertBlockChainOrder(order_details) -> object:
    end_point_url_posts = "https://ccapi.stag.nexuera.com/orders/create"

    billing = order_details['billing']
    shipping = order_details['shipping']

    payload = {
        "order_id": order_details['id'] if order_details['id'] else "",
        "parent_id": order_details['parent_id'] if order_details['parent_id'] else "",
        "state": order_details['status'] if order_details['status'] else "",
        "billing_first_name": billing['first_name'] if billing['first_name'] else "",
        "billing_last_name": billing['last_name'] if billing['last_name'] else "",
        "currency": order_details['currency'] if order_details['currency'] else "",
        "version": order_details['version'] if order_details['version'] else "",
        "date_created": order_details['date_created'] if order_details['date_created'] else "",
        "date_modified": order_details['date_modified'] if order_details['date_modified'] else "",
        "total": order_details['total'] if order_details['total'] else "",
        "total_tax": order_details['total_tax'] if order_details['total_tax'] else "",
        "customer_id": order_details['customer_id'] if order_details['customer_id'] else "",
        "order_key": "",
        "billing_company": billing['company'] if billing['company'] else "",
        "billing_address_1": billing['address_1'] if billing['address_1'] else "",
        "billing_address_2": billing['address_2'] if billing['address_2'] else "",
        "billing_city": billing['city'] if billing['city'] else "",
        "billing_state": billing['state'] if billing['state'] else "",
        "billing_postcode": billing['postcode'] if billing['postcode'] else "",
        "billing_country": billing['country'] if billing['country'] else "",
        "billing_email": billing['email'] if billing['email'] else "",
        "billing_phone": billing['phone'] if billing['phone'] else "",
        "shipping_first_name": shipping['first_name'] if shipping['first_name'] else "",
        "shipping_last_name": shipping['last_name'] if shipping['last_name'] else "",
        "shipping_company": shipping['company'] if shipping['company'] else "",
        "shipping_address_1": shipping['address_1'] if shipping['address_1'] else "",
        "shipping_address_2": shipping['address_2'] if shipping['address_2'] else "",
        "shipping_city": shipping['city'] if shipping['city'] else "",
        "shipping_state": shipping['state'] if shipping['state'] else "",
        "shipping_postcode": shipping['postcode'] if shipping['postcode'] else "",
        "shipping_country": shipping['country'] if shipping['country'] else "",
        "payment_method": order_details['payment_method'] if order_details['payment_method'] else "",
        "payment_method_title": order_details['payment_method_title'] if order_details['payment_method_title'] else "",
        "transaction_id": order_details['transaction_id'] if order_details['transaction_id'] else "",
        "customer_ip_address": order_details['customer_ip_address'] if order_details['customer_ip_address'] else "",
        "created_via": order_details['created_via'] if order_details['created_via'] else "",
        "customer_note": order_details['customer_note'] if order_details['customer_note'] else "",
        "date_completed": "",
        "date_paid": "",
        "cart_hash": order_details['cart_hash'] if order_details['cart_hash'] else "",
        "line_items_id": "",
        "line_items_name": "",
        "line_items_product_id": "",
        "line_items_variation_id": "",
        "line_items_quantity": "",
        "line_items_tax_class": "",
        "line_items_subtotal": "",
        "line_items_subtotal_tax": "",
        "line_items_total": "",
        "line_items_total_tax": "",
        "line_items_taxes": "",
        "line_items_sku": "",
        "line_items_price": "",
        "line_items_parent_name": ""
    }

    try:
        r = requests.post(end_point_url_posts, headers=headers, data=json.dumps(payload), verify=False)
        return r.status_code, r.content
    except Exception as error:
        return 404, str(error)


def insertBlockChainOrderJob(order_details):
    end_point_url_posts = "https://ccapi.stag.nexuera.com/orders/create"


    payload = {
        "order_id": order_details.order_id if order_details.order_id else "",
        "parent_id": order_details.parent_id if order_details.parent_id else "",
        "state": order_details.state if order_details.state else "",
        "billing_first_name": order_details.billing_first_name if order_details.billing_first_name else "",
        "billing_last_name": order_details.billing_last_name if order_details.billing_last_name else "",
        "currency": order_details.currency if order_details.currency else "",
        "version": order_details.version if order_details.version else "",
        "date_created": order_details.date_created.strftime('%Y-%m-%d %H:%M:%S') if order_details.date_created else "",
        "date_modified": order_details.date_modified.strftime('%Y-%m-%d %H:%M:%S') if order_details.date_modified else "",
        "total": order_details.total if order_details.total else "",
        "total_tax": order_details.total_tax if order_details.total_tax else "",
        "customer_id": order_details.customer_id if order_details.customer_id else "",
        "order_key": "",
        "billing_company": order_details.billing_company if order_details.billing_company else "",
        "billing_address_1": order_details.billing_address_1 if order_details.billing_address_1 else "",
        "billing_address_2": order_details.billing_address_2 if order_details.billing_address_2 else "",
        "billing_city": order_details.billing_city if order_details.billing_city else "",
        "billing_state": order_details.billing_state if order_details.billing_state else "",
        "billing_postcode": order_details.billing_postcode if order_details.billing_postcode else "",
        "billing_country": order_details.billing_country if order_details.billing_country else "",
        "billing_email": order_details.billing_email if order_details.billing_email else "",
        "billing_phone": order_details.billing_phone if order_details.billing_phone else "",
        "shipping_first_name": order_details.shipping_first_name if order_details.shipping_first_name else "",
        "shipping_last_name": order_details.shipping_last_name if order_details.shipping_last_name else "",
        "shipping_company": order_details.shipping_company if order_details.shipping_company else "",
        "shipping_address_1": order_details.shipping_address_1 if order_details.shipping_address_1 else "",
        "shipping_address_2": order_details.shipping_address_2 if order_details.shipping_address_2 else "",
        "shipping_city": order_details.shipping_city if order_details.shipping_city else "",
        "shipping_state": order_details.shipping_state if order_details.shipping_state else "",
        "shipping_postcode": order_details.shipping_postcode if order_details.shipping_postcode else "",
        "shipping_country": order_details.shipping_country if order_details.shipping_country else "",
        "payment_method": order_details.payment_method if order_details.payment_method else "",
        "payment_method_title": order_details.payment_method_title if order_details.payment_method_title else "",
        "transaction_id": order_details.transaction_id if order_details.transaction_id else "",
        "customer_ip_address": order_details.customer_ip_address if order_details.customer_ip_address else "",
        "created_via": order_details.created_via if order_details.created_via else "",
        "customer_note": order_details.customer_note if order_details.customer_note  else "",
        "date_completed": "",
        "date_paid": "",
        "cart_hash": order_details.cart_hash if order_details.cart_hash else "",
        "line_items_id": "",
        "line_items_name": "",
        "line_items_product_id": "",
        "line_items_variation_id": "",
        "line_items_quantity": "",
        "line_items_tax_class": "",
        "line_items_subtotal": "",
        "line_items_subtotal_tax": "",
        "line_items_total": "",
        "line_items_total_tax": "",
        "line_items_taxes": "",
        "line_items_sku": "",
        "line_items_price": "",
        "line_items_parent_name": ""
    }

    try:
        r = requests.post(end_point_url_posts, headers=headers, data=json.dumps(payload), verify=False)
        return r.status_code, r.content
    except Exception as error:
        return 404, str(error)


async def insertBlockChainOrderAsync(order_details):
    end_point_url_posts = "https://ccapi.stag.nexuera.com/orders/create"

    billing = order_details['billing']
    shipping = order_details['shipping']

    payload = {
        "order_id": order_details['id'] if order_details['id'] else "",
        "parent_id": order_details['parent_id'] if order_details['parent_id'] else "",
        "state": order_details['status'] if order_details['status'] else "",
        "billing_first_name": billing['first_name'] if billing['first_name'] else "",
        "billing_last_name": billing['last_name'] if billing['last_name'] else "",
        "currency": order_details['currency'] if order_details['currency'] else "",
        "version": order_details['version'] if order_details['version'] else "",
        "date_created": order_details['date_created'] if order_details['date_created'] else "",
        "date_modified": order_details['date_modified'] if order_details['date_modified'] else "",
        "total": order_details['total'] if order_details['total'] else "",
        "total_tax": order_details['total_tax'] if order_details['total_tax'] else "",
        "customer_id": order_details['customer_id'] if order_details['customer_id'] else "",
        "order_key": "",
        "billing_company": billing['company'] if billing['company'] else "",
        "billing_address_1": billing['address_1'] if billing['address_1'] else "",
        "billing_address_2": billing['address_2'] if billing['address_2'] else "",
        "billing_city": billing['city'] if billing['city'] else "",
        "billing_state": billing['state'] if billing['state'] else "",
        "billing_postcode": billing['postcode'] if billing['postcode'] else "",
        "billing_country": billing['country'] if billing['country'] else "",
        "billing_email": billing['email'] if billing['email'] else "",
        "billing_phone": billing['phone'] if billing['phone'] else "",
        "shipping_first_name": shipping['first_name'] if shipping['first_name'] else "",
        "shipping_last_name": shipping['last_name'] if shipping['last_name'] else "",
        "shipping_company": shipping['company'] if shipping['company'] else "",
        "shipping_address_1": shipping['address_1'] if shipping['address_1'] else "",
        "shipping_address_2": shipping['address_2'] if shipping['address_2'] else "",
        "shipping_city": shipping['city'] if shipping['city'] else "",
        "shipping_state": shipping['state'] if shipping['state'] else "",
        "shipping_postcode": shipping['postcode'] if shipping['postcode'] else "",
        "shipping_country": shipping['country'] if shipping['country'] else "",
        "payment_method": order_details['payment_method'] if order_details['payment_method'] else "",
        "payment_method_title": order_details['payment_method_title'] if order_details['payment_method_title'] else "",
        "transaction_id": order_details['transaction_id'] if order_details['transaction_id'] else "",
        "customer_ip_address": order_details['customer_ip_address'] if order_details['customer_ip_address'] else "",
        "created_via": order_details['created_via'] if order_details['created_via'] else "",
        "customer_note": order_details['customer_note'] if order_details['customer_note'] else "",
        "date_completed": "",
        "date_paid": "",
        "cart_hash": order_details['cart_hash'] if order_details['cart_hash'] else "",
        "line_items_id": "",
        "line_items_name": "",
        "line_items_product_id": "",
        "line_items_variation_id": "",
        "line_items_quantity": "",
        "line_items_tax_class": "",
        "line_items_subtotal": "",
        "line_items_subtotal_tax": "",
        "line_items_total": "",
        "line_items_total_tax": "",
        "line_items_taxes": "",
        "line_items_sku": "",
        "line_items_price": "",
        "line_items_parent_name": ""
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with await session.post(end_point_url_posts, headers=headers, data=json.dumps(payload)) as resp:
                return resp.status_code, resp.content
                print(resp.status_code)
                line_item_tx_id = ''
                if int(resp.content[0]) == 200:
                    line_item_tx_id = resp.content[1].decode("utf-8").replace("'", '"')
                else:
                    line_item_tx_id = resp.content[0]
                #   更新tx
                line_items_info_tx = OrdersLineItems.query.filter_by(id=order_details.id).one()
                if line_item_tx_id:
                    line_items_info_tx.tx_id = line_item_tx_id
                db.session.commit()
    except Exception as error:
        return 404, str(error)


def updateBlockChainOrder(order_details):
    end_point_url_posts = "https://ccapi.stag.nexuera.com/orders/update"

    billing = order_details['billing']
    shipping = order_details['shipping']

    payload = {
        "order_id": order_details['id'] if order_details['id'] else "",
        "parent_id": order_details['parent_id'] if order_details['parent_id'] else "",
        "state": order_details['status'] if order_details['status'] else "",
        "billing_first_name": billing['first_name'] if billing['first_name'] else "",
        "billing_last_name": billing['last_name'] if billing['last_name'] else "",
        "currency": order_details['currency'] if order_details['currency'] else "",
        "version": order_details['version'] if order_details['version'] else "",
        "date_created": order_details['date_created'] if order_details['date_created'] else "",
        "date_modified": order_details['date_modified'] if order_details['date_modified'] else "",
        "total": order_details['total'] if order_details['total'] else "",
        "total_tax": order_details['total_tax'] if order_details['total_tax'] else "",
        "customer_id": order_details['customer_id'] if order_details['customer_id'] else "",
        "order_key": "",
        "billing_company": billing['company'] if billing['company'] else "",
        "billing_address_1": billing['address_1'] if billing['address_1'] else "",
        "billing_address_2": billing['address_2'] if billing['address_2'] else "",
        "billing_city": billing['city'] if billing['city'] else "",
        "billing_state": billing['state'] if billing['state'] else "",
        "billing_postcode": billing['postcode'] if billing['postcode'] else "",
        "billing_country": billing['country'] if billing['country'] else "",
        "billing_email": billing['email'] if billing['email'] else "",
        "billing_phone": billing['phone'] if billing['phone'] else "",
        "shipping_first_name": shipping['first_name'] if shipping['first_name'] else "",
        "shipping_last_name": shipping['last_name'] if shipping['last_name'] else "",
        "shipping_company": shipping['company'] if shipping['company'] else "",
        "shipping_address_1": shipping['address_1'] if shipping['address_1'] else "",
        "shipping_address_2": shipping['address_2'] if shipping['address_2'] else "",
        "shipping_city": shipping['city'] if shipping['city'] else "",
        "shipping_state": shipping['state'] if shipping['state'] else "",
        "shipping_postcode": shipping['postcode'] if shipping['postcode'] else "",
        "shipping_country": shipping['country'] if shipping['country'] else "",
        "payment_method": order_details['payment_method'] if order_details['payment_method'] else "",
        "payment_method_title": order_details['payment_method_title'] if order_details['payment_method_title'] else "",
        "transaction_id": order_details['transaction_id'] if order_details['transaction_id'] else "",
        "customer_ip_address": order_details['customer_ip_address'] if order_details['customer_ip_address'] else "",
        "created_via": order_details['created_via'] if order_details['created_via'] else "",
        "customer_note": order_details['customer_note'] if order_details['customer_note'] else "",
        "date_completed": "",
        "date_paid": "",
        "cart_hash": order_details['cart_hash'] if order_details['cart_hash'] else "",
        "line_items_id": "",
        "line_items_name": "",
        "line_items_product_id": "",
        "line_items_variation_id": "",
        "line_items_quantity": "",
        "line_items_tax_class": "",
        "line_items_subtotal": "",
        "line_items_subtotal_tax": "",
        "line_items_total": "",
        "line_items_total_tax": "",
        "line_items_taxes": "",
        "line_items_sku": "",
        "line_items_price": "",
        "line_items_parent_name": ""
    }

    try:
        r = requests.post(end_point_url_posts, headers=headers, data=json.dumps(payload), verify=False)
        return r.status_code, r.content
    except Exception as error:
        return 404, str(error)

def insertBlockChainLineItem(line_items):
    end_point_url_posts = "https://ccapi.stag.nexuera.com/orderitem/create"

    payload = {
        "id": line_items.id if line_items.id else "",
        "order_id": line_items.order_id if line_items.order_id else "",
        "line_items_id": line_items.line_items_id if line_items.line_items_id else "",
        "line_items_name": line_items.line_items_name if line_items.line_items_name else "",
        "line_items_product_id": line_items.line_items_product_id if line_items.line_items_product_id else "",
        "line_items_variation_id": line_items.line_items_variation_id if line_items.line_items_variation_id else "",
        "line_items_quantity": line_items.line_items_quantity if line_items.line_items_quantity else "",
        "line_items_tax_class": line_items.line_items_tax_class if line_items.line_items_tax_class else "",
        "line_items_subtotal": line_items.line_items_subtotal if line_items.line_items_subtotal else "",
        "line_items_subtotal_tax": line_items.line_items_subtotal_tax if line_items.line_items_subtotal_tax else "",
        "line_items_total": line_items.line_items_total if line_items.line_items_total else "",
        "line_items_total_tax": line_items.line_items_total_tax if line_items.line_items_total_tax else "",
        "line_items_taxes": line_items.line_items_taxes if line_items.line_items_taxes else "",
        "line_items_sku": line_items.line_items_sku if line_items.line_items_sku else "",
        "line_items_price": line_items.line_items_price if line_items.line_items_price else "",
        "line_items_parent_name": line_items.line_items_parent_name if line_items.line_items_parent_name else ""
    }

    try:
        r = requests.post(end_point_url_posts, headers=headers, data=json.dumps(payload), verify=False)
        return r.status_code, r.content
    except Exception as error:
        return 404, str(error)

async def insertBlockChainLineItemAsync(line_items):
    end_point_url_posts = "https://ccapi.stag.nexuera.com/orderitem/create"

    payload = {
        "id": line_items.id if line_items.id else "",
        "order_id": line_items.order_id if line_items.order_id else "",
        "line_items_id": line_items.line_items_id if line_items.line_items_id else "",
        "line_items_name": line_items.line_items_name if line_items.line_items_name else "",
        "line_items_product_id": line_items.line_items_product_id if line_items.line_items_product_id else "",
        "line_items_variation_id": line_items.line_items_variation_id if line_items.line_items_variation_id else "",
        "line_items_quantity": line_items.line_items_quantity if line_items.line_items_quantity else "",
        "line_items_tax_class": line_items.line_items_tax_class if line_items.line_items_tax_class else "",
        "line_items_subtotal": line_items.line_items_subtotal if line_items.line_items_subtotal else "",
        "line_items_subtotal_tax": line_items.line_items_subtotal_tax if line_items.line_items_subtotal_tax else "",
        "line_items_total": line_items.line_items_total if line_items.line_items_total else "",
        "line_items_total_tax": line_items.line_items_total_tax if line_items.line_items_total_tax else "",
        "line_items_taxes": line_items.line_items_taxes if line_items.line_items_taxes else "",
        "line_items_sku": line_items.line_items_sku if line_items.line_items_sku else "",
        "line_items_price": line_items.line_items_price if line_items.line_items_price else "",
        "line_items_parent_name": line_items.line_items_parent_name if line_items.line_items_parent_name else ""
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with await session.post(end_point_url_posts, headers=headers, data=json.dumps(payload)) as resp:
                return resp.status_code, resp.content
    except Exception as error:
        return 404, str(error)



def insertBlockChainLineItemJob(line_items):
    end_point_url_posts = "https://ccapi.stag.nexuera.com/orderitem/create"

    payload = {
        "id": line_items.id if line_items.id else "",
        "order_id": line_items.order_id if line_items.order_id else "",
        "line_items_id": line_items.line_items_id if line_items.line_items_id else "",
        "line_items_name": line_items.line_items_name if line_items.line_items_name else "",
        "line_items_product_id": line_items.line_items_product_id if line_items.line_items_product_id else "",
        "line_items_variation_id": line_items.line_items_variation_id if line_items.line_items_variation_id else "",
        "line_items_quantity": line_items.line_items_quantity if line_items.line_items_quantity else "",
        "line_items_tax_class": line_items.line_items_tax_class if line_items.line_items_tax_class else "",
        "line_items_subtotal": line_items.line_items_subtotal if line_items.line_items_subtotal else "",
        "line_items_subtotal_tax": line_items.line_items_subtotal_tax if line_items.line_items_subtotal_tax else "",
        "line_items_total": line_items.line_items_total if line_items.line_items_total else "",
        "line_items_total_tax": line_items.line_items_total_tax if line_items.line_items_total_tax else "",
        "line_items_taxes": line_items.line_items_taxes if line_items.line_items_taxes else "",
        "line_items_sku": line_items.line_items_sku if line_items.line_items_sku else "",
        "line_items_price": line_items.line_items_price if line_items.line_items_price else "",
        "line_items_parent_name": line_items.line_items_parent_name if line_items.line_items_parent_name else ""
    }

    try:
        r = requests.post(end_point_url_posts, headers=headers, data=json.dumps(payload), verify=False)
        return r.status_code, r.content
    except Exception as error:
        return 404, str(error)

def updateBlockChainLineItem(line_items):
    end_point_url_posts = "https://ccapi.stag.nexuera.com/orderitem/update"

    payload = {
        "id": line_items.id if line_items.id else "",
        "order_id": line_items.order_id if line_items.order_id else "",
        "line_items_id": line_items.line_items_id if line_items.line_items_id else "",
        "line_items_name": line_items.line_items_name if line_items.line_items_name else "",
        "line_items_product_id": line_items.line_items_product_id if line_items.line_items_product_id else "",
        "line_items_variation_id": line_items.line_items_variation_id if line_items.line_items_variation_id else "",
        "line_items_quantity": line_items.line_items_quantity if line_items.line_items_quantity else "",
        "line_items_tax_class": line_items.line_items_tax_class if line_items.line_items_tax_class else "",
        "line_items_subtotal": line_items.line_items_subtotal if line_items.line_items_subtotal else "",
        "line_items_subtotal_tax": line_items.line_items_subtotal_tax if line_items.line_items_subtotal_tax else "",
        "line_items_total": line_items.line_items_total if line_items.line_items_total else "",
        "line_items_total_tax": line_items.line_items_total_tax if line_items.line_items_total_tax else "",
        "line_items_taxes": line_items.line_items_taxes if line_items.line_items_taxes else "",
        "line_items_sku": line_items.line_items_sku if line_items.line_items_sku else "",
        "line_items_price": line_items.line_items_price if line_items.line_items_price else "",
        "line_items_parent_name": line_items.line_items_parent_name if line_items.line_items_parent_name else ""
    }

    try:
        r = requests.post(end_point_url_posts, headers=headers, data=json.dumps(payload), verify=False)
        return r.status_code, r.content
    except Exception as error:
        return 404, str(error)


def insertBlockChainInventory(inventory):
    end_point_url_posts = "https://ccapi.stag.nexuera.com/inventory/create"

    payload = {
        "id": inventory.id if inventory.id else "",
        "user_id": inventory.user_id if inventory.user_id else "",
        "beging_inventory": inventory.beging_inventory if inventory.beging_inventory else "",
        "ending_inventory": inventory.ending_inventory if inventory.ending_inventory else "",
        "adj_amount": inventory.adj_amount if inventory.adj_amount else "",
        "create_time": str(inventory.create_time),
        "modify_time": str(inventory.modify_time),
        "transaction_id": inventory.transaction_id if inventory.transaction_id else "",
        "order_id": inventory.order_id if inventory.order_id else "",
        "product_id": inventory.product_id if inventory.product_id else "",
        "create_by": inventory.create_by if inventory.create_by else "",
        "order_source": inventory.order_source if inventory.order_source else "",
        "location": inventory.location if inventory.location else "",
        "shipping_first_name": inventory.shipping_first_name if inventory.shipping_first_name else "",
        "shipping_last_name": inventory.shipping_last_name if inventory.shipping_last_name else "",
        "shipping_company": inventory.shipping_company if inventory.shipping_company else "",
        "shipping_address_1": inventory.shipping_address_1 if inventory.shipping_address_1 else "",
        "shipping_address_2": "",
        "shipping_city": inventory.shipping_city if inventory.shipping_city else "",
        "shipping_postcode": inventory.shipping_postcode if inventory.shipping_postcode else "",
        "shipping_country": inventory.shipping_country if inventory.shipping_country else "",
        "shipping_phone": inventory.shipping_phone if inventory.shipping_phone else "",
        "shipment_number": inventory.shipment_number if inventory.shipment_number else "",
        "remark": inventory.remark if inventory.remark else ""
    }
    print('insert_inventory_bc')
    print(payload)

    try:
        r = requests.post(end_point_url_posts, headers=headers, data=json.dumps(payload), verify=False)
        return r.status_code, r.content
    except Exception as error:
        return 404, str(error)


def updateBlockChainInventory(inventory):
    end_point_url_posts = "https://ccapi.stag.nexuera.com/inventory/update"

    payload = {
        "id": inventory.id if inventory.id else "",
        "user_id": inventory.user_id if inventory.user_id else "",
        "beging_inventory": inventory.beging_inventory if inventory.beging_inventory else "",
        "ending_inventory": inventory.ending_inventory if inventory.ending_inventory else "",
        "adj_amount": inventory.adj_amount if inventory.adj_amount else "",
        "create_time": str(inventory.create_time),
        "modify_time": str(inventory.modify_time),
        "transaction_id": inventory.transaction_id if inventory.transaction_id else "",
        "order_id": inventory.order_id if inventory.order_id else "",
        "product_id": inventory.product_id if inventory.product_id else "",
        "create_by": inventory.create_by if inventory.create_by else "",
        "order_source": inventory.order_source if inventory.order_source else "",
        "location": inventory.location if inventory.location else "",
        "shipping_first_name": inventory.shipping_first_name if inventory.shipping_first_name else "",
        "shipping_last_name": inventory.shipping_last_name if inventory.shipping_last_name else "",
        "shipping_company": inventory.shipping_company if inventory.shipping_company else "",
        "shipping_address_1": inventory.shipping_address_1 if inventory.shipping_address_1 else "",
        "shipping_address_2": "",
        "shipping_city": inventory.shipping_city if inventory.shipping_city else "",
        "shipping_postcode": inventory.shipping_postcode if inventory.shipping_postcode else "",
        "shipping_country": inventory.shipping_country if inventory.shipping_country else "",
        "shipping_phone": inventory.shipping_phone if inventory.shipping_phone else "",
        "shipment_number": inventory.shipment_number if inventory.shipment_number else "",
        "remark": inventory.remark if inventory.remark else ""
    }

    try:
        r = requests.post(end_point_url_posts, headers=headers, data=json.dumps(payload), verify=False)
        return r.status_code, r.content
    except Exception as error:
        return 404, str(error)



def insertBlockChainDelivery(delivery):
    end_point_url_posts = "https://ccapi.stag.nexuera.com/delivery/create"

    payload = {
        "id": delivery.id if delivery.id else "",
        "user_id": delivery.user_id if delivery.user_id else "",
        "create_time": str(delivery.create_time),
        "modify_time": str(delivery.modify_time),
        "create_by": delivery.create_by if delivery.create_by else "",
        "order_source": delivery.order_source if delivery.order_source else "",
        "location": delivery.location if delivery.location else "",
        "shipping_first_name": delivery.shipping_first_name if delivery.shipping_first_name else "",
        "shipping_last_name": delivery.shipping_last_name if delivery.shipping_last_name else "",
        "shipping_company": delivery.shipping_company if delivery.shipping_company else "",
        "shipping_address_1": delivery.shipping_address_1 if delivery.shipping_address_1 else "",
        "shipping_address_2": delivery.shipping_address_2 if delivery.shipping_address_2 else "",
        "shipping_city": delivery.shipping_city if delivery.shipping_city else "",
        "shipping_state": delivery.shipping_state if delivery.shipping_state else "",
        "shipping_postcode": delivery.shipping_postcode if delivery.shipping_postcode else "",
        "shipping_country": delivery.shipping_country if delivery.shipping_country else "",
        "shipping_phone": delivery.shipping_phone if delivery.shipping_phone else "",
        "shipment_number": delivery.shipment_number if delivery.shipment_number else "",
        "remark": delivery.remark if delivery.remark else ""
    }

    try:
        r = requests.post(end_point_url_posts, headers=headers, data=json.dumps(payload), verify=False)
        return r.status_code, r.content
    except Exception as error:
        return 404, str(error)



def updateBlockChainDelivery(delivery):
    end_point_url_posts = "https://ccapi.stag.nexuera.com/delivery/update"

    payload = {
        "id": delivery.id,
        "user_id": delivery.user_id,
        "create_time": delivery.create_time,
        "modify_time": delivery.modify_time,
        "create_by": delivery.create_by,
        "order_source": delivery.order_source,
        "location": delivery.location,
        "shipping_first_name": delivery.shipping_first_name,
        "shipping_last_name": delivery.shipping_last_name,
        "shipping_company": delivery.shipping_company,
        "shipping_address_1": delivery.shipping_address_1,
        "shipping_address_2": delivery.shipping_address_2,
        "shipping_city": delivery.shipping_city,
        "shipping_state": delivery.shipping_state,
        "shipping_postcode": delivery.shipping_postcode,
        "shipping_country": delivery.shipping_country,
        "shipping_phone": delivery.shipping_phone,
        "shipment_number": delivery.shipment_number,
        "remark": delivery.remark
    }

    try:
        r = requests.post(end_point_url_posts, headers=headers, data=json.dumps(payload), verify=False)
        return r.status_code, r.content
    except Exception as error:
        return 404, str(error)


def getOrderDetail(order_id):
    r = requests.post(end_point_url_posts, data=payload)
    jwt_info = r.content.decode("utf-8").replace("'", '"')
    data = json.loads(jwt_info)
    my_headers = {'Authorization': "Bearer " + data['token']}
    res_order_details = requests.get('https://store.pyrarc.com/wp-json/wc/v3/orders/' + str(order_id),
                                     data=payload,
                                     headers=my_headers)
    if not res_order_details:
        return None
    order_details = json.loads(res_order_details.content.decode("utf-8").replace("'", '"'))
    return order_details
