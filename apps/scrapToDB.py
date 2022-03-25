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

    def get_nonExisted_index(self):
        q = QueryTable(self.db).get(sql='select rceptNo from consolidatedData')
        self.existed_lst = [i.rceptNo for i in q]

        for i in self.lst:
            if not i.rcept_no in self.existed_lst:
                return self.lst.index(i)

    def delete_edge_data(self, i):
        _rcept_no = self.lst[i].rcept_no
        c = self.db.cursor()
        sql = f'delete from consolidatedData where rceptNo = {_rcept_no}'
        c.execute(sql)
        sql = f'delete from nonConsolidatedData where rceptNo = {_rcept_no}'
        try :
            c.execute(sql)
        except:
            pass
        self.db.commit()


    def operate(self, lst):
        self.lst = lst

        ic = Insert_ConsolidatedData(self.db)
        inc = Insert_NonConsolidatedData(self.db)

        i = self.get_nonExisted_index()

        if not i == 0:
            self.delete_edge_data(i-1)
            nonExisted_lst = lst[i-1:]
        else:
            nonExisted_lst = lst[i:]

        n = 1
        total = len(lst)
        for w in nonExisted_lst:
            print(f'{n+i-1}/{total}', w, sep='\n')
            fd = FundamentalData(w.rcept_no)
            ic.operate(fd.consolidatedData)
            inc.operate(fd.nonConsolidatedData)
            n += 1

def main():

    dbName = 'fundamentalData'
    db = Connector().connect_db(dbName)
    
    # CorpCodeScrapToDB(db).operate()

    # corp_code = [data.corp_code for data in QueryTable(db).get(tableName='corpCode')]
    # start = '20100101'
    # end = '20211130'
    # RceptNoInfoScrapToDB(db).operate(corp_code, start, end)

    rceptno_lst = QueryTable(db).get(sql='select rcept_no, corp_name from rceptNoInfo where add_info != "첨부정정"')
    DataScrapToDB(db).operate(list(rceptno_lst))


if __name__ == '__main__':
    main()