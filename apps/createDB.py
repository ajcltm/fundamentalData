parentPath='c:/Users/ajcltm/PycharmProjects/fundamentalData'
import sys
sys.path.append(parentPath)
from abc import abstractmethod
from dbManagement.connectDB import Connector

class CreateTable:

    def __init__(self, connectedDB) -> None:
        self.db = connectedDB

    @abstractmethod
    def operate(self):
        pass

class CorpCodeTable(CreateTable):

    def operate(self):
        
        sql = "CREATE TABLE IF NOT EXISTS corpCode(\
                corp_code VARCHAR(8),\
                corp_name VARCHAR(100),\
                stock_code VARCHAR(6),\
                modify_date TIMESTAMP\
            )"
        
        self.db.cursor().execute(sql)
        self.db.commit()

class RceptNoInfoTable(CreateTable):

    def operate(self):
        
        sql = "CREATE TABLE IF NOT EXISTS rceptNoInfo(\
                corp_code VARCHAR(8),\
                corp_name VARCHAR(100),\
                stock_code VARCHAR(6),\
                corp_cls VARCHAR(5),\
                report_nm VARCHAR(50),\
                rcept_no VARCHAR(14),\
                flr_nm VARCHAR(100),\
                rcept_dt VARCHAR(8),\
                rm VARCHAR(20),\
                add_info VARCHAR(20),\
                kind VARCHAR(20),\
                date TIMESTAMP\
            )"
        
        self.db.cursor().execute(sql)
        self.db.commit()

class ConsolidatedDataTable(CreateTable) :

    def operate(self) -> None:

        sql = "CREATE TABLE IF NOT EXISTS consolidatedData(\
                rceptNo VARCHAR(14),\
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
                rceptNo VARCHAR(14),\
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
                rceptNo VARCHAR(14),\
                html MEDIUMTEXT\
                )"

        self.db.cursor().execute(sql)
        self.db.commit()


class NonConsolidatedReportTable(CreateTable) :

    def operate(self) -> None:

        sql = "CREATE TABLE IF NOT EXISTS NonConsolidatedReport(\
                rceptNo VARCHAR(14),\
                html MEDIUMTEXT\
                )"

        self.db.cursor().execute(sql)
        self.db.commit()


def main():
    dbName = 'fundamentalData'
    db = Connector().connect_db(dbName)
    CorpCodeTable(db).operate()
    RceptNoInfoTable(db).operate()
    ConsolidatedDataTable(db).operate()
    NonConsolidatedDataTable(db).operate()
    ConsolidatedReportTable(db).operate()
    NonConsolidatedReportTable(db).operate()
    db.close()


if __name__ == '__main__':
    main()
