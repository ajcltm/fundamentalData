from abc import abstractmethod
from rceptNoInfo import RceptNoInfoProvider
from fundamentalData import FundamentalData
from dbMangement.connectDB import Connector
from dbMangement.insertDB import Insert_corpCode, Insert_RceptNoInfo, Insert_ConsolidatedData, Insert_NonConsolidatedData, Insert_ConsolidatedReport, Insert_NonConsolidatedReport
from corpCode import CorpCode
from tqdm import tqdm

class CorpCodeScraper:

    def __init__(self, connectedDB):
        self.db = connectedDB

    def operate(self):
        ic = Insert_corpCode(self.db)
        cc = CorpCode()
        cc.downloadXmlFile()
        dcs = cc.get_dcs()

        for data in tqdm(dcs, bar_format='{l_bar}{bar:20}{r_bar}{bar:-20b}'):
            ic.operate(data)

class RceptNoInfoScraper:

    def __init__(self, connectedDB):
        self.db = connectedDB

    def operate(self, lst, start, end):
        ri = RceptNoInfoProvider()
        ir = Insert_RceptNoInfo(self.db)
        for corp_code in lst:
            gen = ri.get_generator(corp_code, start, end)
            for data in gen:
                ir.operate(data)


class DataScraper:

    def __init__(self, connectedDB):
        self.db = connectedDB

    def operate(self, lst):
        ic = Insert_ConsolidatedData(self.db)
        inc = Insert_NonConsolidatedData(self.db)
        icr = Insert_ConsolidatedReport(self.db)
        incr = Insert_NonConsolidatedReport(self.db)

        for i in lst:
            fd = FundamentalData(i)
            ic.operate(fd.consolidatedData)
            inc.operate(fd.nonConsolidatedData)
            # icr.operate(fd.consolidatedHtml)
            # incr.operate(fd.nonConsolidatedHtml)


def main():
    dbName = 'fundamentalData'
    db = Connector().connect_db(dbName)
    
    CorpCodeScraper(db).operate()

    # corp_code = ['005930']
    # start = '20100101'
    # end = '20211130'
    # RceptNoInfoScraper(db).operate(corp_code, start, end)

    # receptNos = ['20201116001840', '20100816001298', '20200928000281', '20180515001679']
    # DataScraper(db).operate(receptNos)


if __name__ == '__main__':
    main()