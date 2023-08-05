from dataclasses import dataclass
from datetime import date, time, datetime


@dataclass
class Product:
    id: int
    rate: float
    status: str
    amount: int
    term: int
    name: str
    recommend: str
    gmt_create: date

    def __init__(self):
        self.id = 0
        self.rate = 0.0
        self.status = ''
        self.amount = 0
        self.recommend = ''
        self.term = 0
        self.name = ''
        self.gmt_create = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        pass

    def __str__(self):

        message = '米庄新产品上线：\n' \
                  '名称: %s\n' \
                  '利率: %.3f%%\n'\
                  '服务期: %d\n' \
                  '时间: %s \n' \
                  '' % (self.name, self.rate * 100, self.term, self.gmt_create)

        return message
