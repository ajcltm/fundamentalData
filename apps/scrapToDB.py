parentPath='c:/Users/ajcltm/PycharmProjects/fundamentalData'
import sys
sys.path.append(parentPath)
from dartScraper.rceptNoInfo import RceptNoInfoProvider
from apps.fundamentalData import FundamentalData
from dbManagement.connectDB import Connector
from dbManagement.insertDB import Insert_corpCode, Insert_RceptNoInfo, Insert_ConsolidatedData, Insert_NonConsolidatedData, Insert_ConsolidatedReport, Insert_NonConsolidatedReport
from dbManagement.queryDB import QueryTable
from dartScraper.corpCode import CorpCodeScraper
from tqdm import tqdm

class CorpCodeScrapToDB:

    def __init__(self, connectedDB):
        self.db = connectedDB

    def operate(self):
        ic = Insert_corpCode(self.db)
        cc = CorpCodeScraper()
        cc.downloadXmlFile()
        dcs = cc.get_dcs()

        for data in tqdm(dcs, bar_format='{l_bar}{bar:20}{r_bar}{bar:-20b}'):
            ic.operate(data)

class RceptNoInfoScrapToDB:

    def __init__(self, connectedDB):
        self.db = connectedDB

    def get_nonExisted_lst(self, lst):
        data_lst = QueryTable(self.db).get(tableName='rceptNoInfo')
        existed_lst = list(set([data.corp_code for data in data_lst]))
        return [i for i in lst if not i in existed_lst]

    def operate(self, lst, start, end):
        ri = RceptNoInfoProvider()
        ir = Insert_RceptNoInfo(self.db)
        nonExisted_lst = self.get_nonExisted_lst(lst)
        print(nonExisted_lst[0])
        for corp_code in tqdm(nonExisted_lst, bar_format='{l_bar}{bar:20}{r_bar}{bar:-20b}'):
            gen = ri.get_generator(corp_code, start, end)
            if not gen:
                # print('failed to get rceptNoInfo',
                #     QueryTable(self.db).get(tableName='corpCode', where=f'where corp_code={corp_code}')[0],
                #     sep='\n')
                continue
            for data in gen:
                ir.operate(data)

class DataScrapToDB:

    def __init__(self, connectedDB):
        self.db = connectedDB

    def get_nonExisted_lst(self, lst):
        data_lst = QueryTable(self.db).get(tableName='consolidatedData')
        existed_lst = list(set([data.rceptNo for data in data_lst]))
        return [i for i in lst if not i in existed_lst]

    def operate(self, lst):
        ic = Insert_ConsolidatedData(self.db)
        inc = Insert_NonConsolidatedData(self.db)
        # icr = Insert_ConsolidatedReport(self.db)
        # incr = Insert_NonConsolidatedReport(self.db)

        nonExisted_lst = self.get_nonExisted_lst(lst)

        n = 0
        total = len(nonExisted_lst)
        for i in nonExisted_lst:
            print(n, f'{n/total}', i, sep='\n')
            
            fd = FundamentalData(i)
            ic.operate(fd.consolidatedData)
            inc.operate(fd.nonConsolidatedData)
            # icr.operate(fd.consolidatedHtml)
            # incr.operate(fd.nonConsolidatedHtml)
            n += 1

def main():
    import time

    dbName = 'fundamentalData'
    db = Connector().connect_db(dbName)
    
    # CorpCodeScrapToDB(db).operate()

    # corp_code = [data.corp_code for data in QueryTable(db).get(tableName='corpCode')]
    # start = '20100101'
    # end = '20211130'
    # RceptNoInfoScrapToDB(db).operate(corp_code, start, end)
    s = time.time()
    # rceptno_lst = list(set([data.rcept_no for data in QueryTable(db).get(tableName='rceptNoInfo')]))
    q = QueryTable(db).get(sql='select corp_name, rcept_no from rceptNoInfo')
    print(list(q)[-2:])
    # rceptno_lst = [data.rcept_no for data in QueryTable(db).get(tableName='rceptNoInfo')]
    # print(rceptno_lst[:1])
    
    # DataScrapToDB(db).operate(rceptno_lst)
    # DataScrapToDB(db).operate(receptNos)

    e = time.time()
    print(f'duration : {e -s} seconds')


if __name__ == '__main__':
    main()