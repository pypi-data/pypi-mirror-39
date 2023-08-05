import sqlite3
import sys
from getopt import getopt
from sys import stdout
from traceback import print_exc

from kit import version
from mizlicai.model import Product

from kit.db.db_helper import create_table_if_need
from mizlicai import db_name

from mizlicai.product import check_new_product


def main():
    result = True
    conn = sqlite3.connect(db_name)
    try:
        opts, args = getopt(sys.argv[1:], "htv")
        for op, value in opts:
            if op == '-h':
                usage()
                exit(0)
            elif op == '-t':
                create_table_if_need(Product(), conn)
                exit(0)
            elif op == '-v':
                print('mizlicai: %s' % (version()))
                exit(0)
        create_table_if_need(Product(), conn)
        check_new_product(conn)
    except Exception:
        # Flush the problems we have printed so far to avoid the traceback
        # appearing in between them.
        stdout.flush()
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


def usage():
    pass
