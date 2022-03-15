from fundamentalData import FundamentalData
from dbMangement.connectDB import Connector
from dbMangement.insertDB import Insert_ConsolidatedData, Insert_NonConsolidatedData, Insert_ConsolidatedReport, Insert_NonConsolidatedReport


class Scrapper:

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
    receptNos = ['20201116001840', '20100816001298', '20200928000281', '20180515001679']
    Scrapper(db).operate(receptNos)


if __name__ == '__main__':
    main()