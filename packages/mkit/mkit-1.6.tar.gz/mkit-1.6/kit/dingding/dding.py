import sqlite3
import sys
from getopt import getopt
from traceback import print_exc

from mizlicai.product import check_new_product

from kit import version
from kit.db.db_helper import create_table_if_need
from kit.dingding import db_name
from kit.dingding.user import user


def usage():
    print("-h 打印当前帮着")
    print("-v 打印版本号")
    print("-u 更新部门人员数据库")
    pass


def main():
    result = True
    conn = sqlite3.connect(db_name)
    try:
        opts, args = getopt(sys.argv[1:], "a:huv")
        for op, value in opts:
            if op == '-h':
                usage()
                exit(0)
            elif op == '-v':
                print('dding: %s' % (version()))
                exit(0)
        create_table_if_need(user(), conn)
    except Exception:
        # Flush the problems we have printed so far to avoid the traceback
        # appearing in between them.
        sys.stdout.flush()
        print(file=sys.stderr)
        print('An error occurred, but the commits are accepted.', file=sys.stderr)
        print_exc()
        result = False
    finally:
        if conn is not None:
            conn.close()
        if result:
            """ 0表示成功 """
            print(0)
        else:
            """ 1表示失败 """
            print(1)