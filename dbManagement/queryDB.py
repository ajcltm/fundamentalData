parentPath='c:/Users/ajcltm/PycharmProjects/fundamentalData'
import sys
sys.path.append(parentPath)
from dbManagement.models import CorpCodeData, RceptNoInfo, ConsolidatedDataDC, NonConsolidatedDataDC, HtmlDC
from typing import List
from abc import abstractmethod
from dbManagement.models import CorpCodeData, RceptNoInfo, ConsolidatedDataDC, NonConsolidatedDataDC, HtmlDC
from typing import List
from abc import abstractmethod



class QueryTable:

    def __init__(self, connectedDB):
        self.db = connectedDB
        self.dataDict = {'corpCode' : CorpCodeData,
                        'rceptNoInfo' : RceptNoInfo,
                        'consolidatedData' : ConsolidatedDataDC,
                        'nonConsolidatedData' : NonConsolidatedDataDC,
                        'consolidatedReport' : HtmlDC,
                        'nonConsolidatedReport' : HtmlDC}

    def get(self, tableName, where=None) -> List[CorpCodeData]:
        if where:
            sql = f'select * from {tableName} {where}'
        else:
            sql = f'select * from {tableName}'
        c = self.db.cursor()
        c.execute(sql)
        data_class = self.dataDict.get(tableName)
        data = [data_class(**{key: data[i] for i, key in enumerate(data_class.__fields__.keys())}) for data in c.fetchall()]
        return data
