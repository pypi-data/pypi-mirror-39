import datetime
import time

import requests
import json

from kit.dingding.notify import get_access_token, get_dept_member, get_user, send_text_to_users
from mizlicai import new_product_url, unique_id, recommend, total_amount, sold_amount, rate, status, name, term
from kit.db.db_helper import insert, query
from mizlicai.model import Product


def dd_notify(message):
    token = get_access_token()
    for user_id in get_dept_member(token):
        # print(get_user(token, user_id))
        send_text_to_users(token, [user_id], message)
        return
    pass


def check_new_product():
    result = requests.get(new_product_url)
    jsonObj = json.loads(result.text, encoding='utf-8')
    products = jsonObj['normalProductOnsell']

    for product in products:
        lastProduct = Product()
        lastProduct.id = product[unique_id]
        lastProduct.recommend = product[recommend]
        lastProduct.amount = int(product[total_amount]) - int(product[sold_amount])
        lastProduct.rate = float(product[rate])
        lastProduct.status = product[status]
        lastProduct.name = product[name]
        lastProduct.term = product[term]
        has_notify = False
        if query(lastProduct) is None:
            if insert(lastProduct):
                dd_notify(lastProduct.__str__())
                has_notify = True
        else:
            print(lastProduct.__str__() + " already exist")
        if not has_notify:
            dd_notify(time.time())

