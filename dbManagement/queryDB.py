parentPath='c:/Users/ajcltm/PycharmProjects/fundamentalData'
import sys
sys.path.append(parentPath)
from abc import abstractmethod
from typing import List
import dataclasses


class QueryTable:

    def __init__(self, connectedDB):
        self.db = connectedDB

    def get(self, sql) -> List:
        c = self.db.cursor()
        c.execute(sql)
        attr = self.get_attr(sql)
        _dataclass = dataclasses.make_dataclass('Data', attr)
        data = (_dataclass(**{key: data[i] for i, key in enumerate(attr)}) for data in c.fetchall())
        return data

    def get_attr(self, sql):
        sql = sql.replace(',', '')
        lst = sql.split()
        s = lst.index('select')
        e = lst.index('from')
        attr = lst[s+1:e]
        return attr
