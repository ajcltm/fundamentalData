parentPath='c:/Users/ajcltm/PycharmProjects/fundamentalData'
import sys

from numpy import where
sys.path.append(parentPath)
from dbManagement.queryDB import QueryTable
sys.path.append(parentPath)
from dbManagement.connectDB import Connector
from dbManagement.queryDB import QueryTable
import pandas as pd
import webbrowser



if __name__ == '__main__':
    dbName = 'fundamentalData'
    db = Connector().connect_db(dbName)
    tableName = 'rceptNoInfo'
    where = "where corp_name like '현대자동%'"
    q = QueryTable(db).get(tableName=tableName, where=where)
    q = [i.dict() for i in q]
    print(pd.DataFrame(q))
    # print(QueryTable(db).get(tableName='corpCode')[:2])
    # print(QueryTable(db).get(tableName='corpCode', where='where stock_code = 005930')[0])

    # html = QueryConsolidatedReport(db).get(rceptNo='20201116001840')[0].html

    # filepath = "c:/Users/ajcltm/PycharmProjects/fundamentalData/hello.html"
    # with open(filepath, 'w', encoding='utf8') as f:
    #     f.write(html)
    #     f.close()
 
    # webbrowser.open_new_tab(filepath)