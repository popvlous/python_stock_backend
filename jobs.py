from app import app
from model import Orders, db, OrdersLineItems
from util import insertBlockChainOrder, insertBlockChainOrderJob, insertBlockChainLineItemJob


def bcjob():
    #上鏈訂單master
    with app.app_context():
        order_infos = Orders.query.filter_by(tx_id="0").all()
        for order_info in order_infos:
            print(order_info.id)
            bc_info = insertBlockChainOrderJob(order_info)
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

def bclitemjob():
    #上鏈訂單detail
    with app.app_context():
        line_items_infos = OrdersLineItems.query.filter_by(tx_id="0").all()
        for line_items_info in line_items_infos:
            print(line_items_info)
            bc_info = insertBlockChainLineItemJob(line_items_info)
            line_item_tx_id = ''
            if int(bc_info[0]) == 200:
                line_item_tx_id = bc_info[1].decode("utf-8").replace("'", '"')
            else:
                line_item_tx_id = bc_info[0]
            #   更新tx
            order_info_tx = OrdersLineItems.query.filter_by(id=line_items_info.id).one()
            if line_item_tx_id:
                order_info_tx.tx_id = line_item_tx_id
            db.session.commit()