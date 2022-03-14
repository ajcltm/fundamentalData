import pymysql

class CreateDB :

    def __init__(self) -> None:
        self.db = self.get_db()

    def get_db(self) :
        self.db = pymysql.connect(host='localhost', port=3306, user='root', passwd='2642805', db='fundamentalData', charset='utf8')
        return self.db

    def createTable_consolidateData(self) -> None:
    
        sql = "CREATE TABLE IF NOT EXISTS consolidateData(\
                receptNo VARCHAR(14),\
                consolidatedEquity INT,\
                consolidatedliability INT,\
                consolidatedNetIncome INT,\
                consolidatedGrossProfit INT,\
                consolidatedOperatiGrossProfit INT,\
                consolidatedOperatingProfit INT,\
                consolidatedConprehensiveNetIncome INT,\
                consolidatedConprehensiveGrossProfit INT,\
                consolidatedConprehensiveOperatingProfit INT,\
                consolidatedOperatingActivities INT\
                )"

        self.db.cursor().execute(sql)
        self.db.commit()
        self.db.close()

if __name__ == '__main__':
    CreateDB().createTable_consolidateData()
