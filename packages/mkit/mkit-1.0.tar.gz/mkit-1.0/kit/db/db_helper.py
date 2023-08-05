import sqlite3

from mizlicai import db_name, model
from mizlicai.model import Product


def create_table(obj: object):
    """
        根据任意对象obj成员对象来创建表
        obj的成员对象必须赋初始值
    """
    table_name = obj.__class__.__name__
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    sql = 'create table %s ( id   int primary key  not null, ' % table_name
    for attr in dir(obj):
        if attr.startswith('__') and attr.endswith('__'):
            continue
        if attr == 'id':
            continue
        sql += attr + "   " + obj.__getattribute__(attr).__class__.__name__ + ","

    length = len(sql)
    sql = sql[0: length - 1]
    sql += ");"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def insert(obj: object):
    table_name = obj.__class__.__name__

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    attrs = [attr for attr in dir(obj) if not attr.startswith('__') and not attr.endswith('__')]
    attrs_name = ','.join(attrs)

    values = ''
    for attr in attrs:
        attr_value = obj.__getattribute__(attr)
        if attr_value.__class__ == str:
            values += "'%s'," % attr_value
        else:
            values += str(attr_value) + ","
    attrs_value = values[0: len(values) - 1]
    sql = 'insert into %s (%s) values (%s)' % (table_name, attrs_name, attrs_value)

    try:
        cursor.execute(sql)
    except Exception:
        return False

    conn.commit()
    cursor.close()
    conn.close()
    return True


def query(obj: object):
    """
    搜索
    :param obj: 搜索对象
    :return: 搜索结果
    """
    table_name = obj.__class__.__name__

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("select * from %s where id = %d" % (table_name, obj.id))

    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return result


'''
rate = 'interestRate'  # 利率

term = 'term'  # 服务期，服务天数

status = 'status'  # 销售状态 ONSELL

total_amount = 'totalAmount'  # 总金额

sold_amount = 'soldAmount'   # 已售出金额

recommend = 'recommend'  # 产品推荐说明
'''
