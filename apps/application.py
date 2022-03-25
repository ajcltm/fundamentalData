parentPath='c:/Users/ajcltm/PycharmProjects/fundamentalData'
import sys
sys.path.append(parentPath)
from dbManagement.connectDB import Connector
from dbManagement.queryDB import QueryTable
import pandas as pd
import webbrowser
from apps.fundamentalData import FundamentalData
import requests


if __name__ == '__main__':
    # dbName = 'fundamentalData'
    # db = Connector().connect_db(dbName)
    # tableName = 'rceptNoInfo'
    # where = "where corp_name like '삼성전자'"
    # q = QueryTable(db).get(tableName=tableName, where=where)
    # q = [i.dict() for i in q]
    # print(pd.DataFrame(q))
    # print(QueryTable(db).get(tableName='corpCode')[:2])
    # print(QueryTable(db).get(tableName='corpCode', where='where stock_code = 005930')[0])

    # html = QueryConsolidatedReport(db).get(rceptNo='20201116001840')[0].html
    # data = FundamentalData('20150105000031')
    # filepath = "c:/Users/ajcltm/PycharmProjects/fundamentalData/hello.html"
    # with open(filepath, 'w', encoding='utf8') as f:
    #     f.write(data.nonConsolidatedHtml.html.prettify())
    #     f.close()
 
    # webbrowser.open_new_tab(filepath)
    dbName = 'fundamentalData'
    db = Connector().connect_db(dbName)
    q = QueryTable(db).get(sql='select corp_name, add_info from rceptNoInfo where rcept_no = 20100223000281')
    print(list(q))
    # f = FundamentalData('20120515001628')
    # print(f.nonConsolidatedData)