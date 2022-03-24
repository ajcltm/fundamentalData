parentPath='c:/Users/ajcltm/PycharmProjects/fundamentalData'
import sys
sys.path.append(parentPath)
from dbManagement.models import CorpCodeData, RceptNoInfo, ConsolidatedDataDC, NonConsolidatedDataDC, HtmlDC
from typing import List
from abc import abstractmethod
from dbManagement.models import CorpCodeData, RceptNoInfo, ConsolidatedDataDC, NonConsolidatedDataDC, HtmlDC
from typing import List
from abc import abstractmethod
from pydantic import BaseModel



class QueryTable:

    def __init__(self, connectedDB):
        self.db = connectedDB
        self.dataDict = {'corpCode' : CorpCodeData,
                        'rceptNoInfo' : RceptNoInfo,
                        'consolidatedData' : ConsolidatedDataDC,
                        'nonConsolidatedData' : NonConsolidatedDataDC,
                        'consolidatedReport' : HtmlDC,
                        'nonConsolidatedReport' : HtmlDC}

    def get(self, sql) -> List[CorpCodeData]:
        c = self.db.cursor()
        c.execute(sql)
        attr, name = self.get_attr(sql)
        attr_dct = {i : "-" for i in attr}
        data_class = type(name, (BaseModel,), attr_dct)
        # data = [data_class(**{key: data[i] for i, key in enumerate(data_class.__fields__.keys())}) for data in c.fetchall()]
        data = (data_class(**{key: data[i] for i, key in enumerate(attr)}) for data in c.fetchall())
        return data

    def get_attr(self, sql):
        lst = sql.split()
        s = lst.index('select')
        e = lst.index('from')
        attr = lst[s+1:e]
        name = lst[e+1]
        return attr, name
