import sys
from sys import stdout
from traceback import print_exc

from mizlicai.product import check_new_product


def main():
    result = True
    try:
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
