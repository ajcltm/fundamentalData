from abc import abstractmethod
from connectDB import Connector

class CreateTable:

    def __init__(self, connectedDB) -> None:
        self.db = connectedDB

    @abstractmethod
    def operate(self):
        pass


class ConsolidatedDataTable(CreateTable) :

    def operate(self) -> None:

        sql = "CREATE TABLE IF NOT EXISTS consolidatedData(\
                receptNo VARCHAR(14),\
                consolidatedEquity BIGINT,\
                consolidatedliability BIGINT,\
                consolidatedNetIncome BIGINT,\
                consolidatedGrossProfit BIGINT,\
                consolidatedOperatingProfit BIGINT,\
                consolidatedConprehensiveNetIncome BIGINT,\
                consolidatedConprehensiveGrossProfit BIGINT,\
                consolidatedConprehensiveOperatingProfit BIGINT,\
                consolidatedOperatingActivities BIGINT\
                )"

        self.db.cursor().execute(sql)
        self.db.commit()

class NonConsolidatedDataTable(CreateTable) :

    def operate(self) -> None:

        sql = "CREATE TABLE IF NOT EXISTS NonConsolidatedData(\
                receptNo VARCHAR(14),\
                NonConsolidatedEquity BIGINT,\
                NonConsolidatedliability BIGINT,\
                NonConsolidatedNetIncome BIGINT,\
                NonConsolidatedGrossProfit BIGINT,\
                NonConsolidatedOperatingProfit BIGINT,\
                NonConsolidatedConprehensiveNetIncome BIGINT,\
                NonConsolidatedConprehensiveGrossProfit BIGINT,\
                NonConsolidatedConprehensiveOperatingProfit BIGINT,\
                NonConsolidatedOperatingActivities BIGINT\
                )"

        self.db.cursor().execute(sql)
        self.db.commit()

class ConsolidatedReportTable(CreateTable) :

    def operate(self) -> None:

        sql = "CREATE TABLE IF NOT EXISTS ConsolidatedReport(\
                receptNo VARCHAR(14),\
                html VARCHAR(4000)\
                )"

        self.db.cursor().execute(sql)
        self.db.commit()


class NonConsolidatedReportTable(CreateTable) :

    def operate(self) -> None:

        sql = "CREATE TABLE IF NOT EXISTS NonConsolidatedReport(\
                receptNo VARCHAR(14),\
                html VARCHAR(4000)\
                )"

        self.db.cursor().execute(sql)
        self.db.commit()


def main():
    dbName = 'fundamentalData'
    db = Connector().connect_db(dbName)
    ConsolidatedDataTable(db).operate()
    NonConsolidatedDataTable(db).operate()
    ConsolidatedReportTable(db).operate()
    NonConsolidatedReportTable(db).operate()
    db.close()


if __name__ == '__main__':
    main()
