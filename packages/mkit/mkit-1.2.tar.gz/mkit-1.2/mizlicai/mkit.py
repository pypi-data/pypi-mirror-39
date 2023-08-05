import sys
from getopt import getopt
from sys import stdout
from traceback import print_exc

from mizlicai.model import Product

from kit.db.db_helper import create_table
from mizlicai import VERSION

from mizlicai.product import check_new_product


def main():
    result = True
    try:
        opts, args = getopt(sys.argv[1:], "htv")
        for op, value in opts:
            if op == '-h':
                usage()
                exit(0)
            elif op == 't':
                create_table(Product())
                exit(0)
            elif op == '-v':
                print('mizlicai: %s' % (version()))
                exit(0)
        check_new_product()
    except Exception:
        # Flush the problems we have printed so far to avoid the traceback
        # appearing in between them.
        stdout.flush()
        print(file=sys.stderr)
        print('An error occurred, but the commits are accepted.', file=sys.stderr)
        print_exc()
    if result:
        """ 0表示成功 """
        print(0)
    else:
        """ 1表示失败 """
        print(1)


def usage():
    pass


def version():
    return '.'.join(str(v) for v in VERSION)
