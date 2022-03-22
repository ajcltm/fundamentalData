parentPath='c:/Users/ajcltm/PycharmProjects/fundamentalData'
import sys
sys.path.append(parentPath)
from dbManagement.models import HtmlDC

from abc import abstractmethod
from datetime import datetime

class InsertData:

    def __init__(self, connectedDB):
        self.db = connectedDB

    @abstractmethod
    def operate(self, data):
        pass

class Insert_corpCode(InsertData):

    def operate(self, data):
        values_part = formatter().get_values_part(data)
        sql = f"insert into corpCode values ({values_part})"
        try:
            self.db.cursor().execute(sql)
        except :
            raise Exception()
        self.db.commit()

class Insert_RceptNoInfo(InsertData):

    def operate(self, data):
        values_part = formatter().get_values_part(data)
        sql = f"insert into RceptNoInfo values ({values_part})"
        self.db.cursor().execute(sql)
        self.db.commit()

class Insert_ConsolidatedData(InsertData):

    def operate(self, data):
        values_part = formatter().get_values_part(data)
        sql = f"insert into consolidatedData values ({values_part})"
        self.db.cursor().execute(sql)
        self.db.commit()

class Insert_NonConsolidatedData(InsertData):

    def operate(self, data):
        values_part = formatter().get_values_part(data)
        sql = f"insert into NonConsolidatedData values\
                ({values_part})"
        self.db.cursor().execute(sql)
        self.db.commit()

class Insert_ConsolidatedReport(InsertData):

    def get_html(self, html):
        if not html:
            return None
        return html.prettify()

    def operate(self, data):
        html = self.get_html(data.html)
        values_part = formatter().get_values_part(HtmlDC(rceptNo=data.rceptNo, html=html))
        sql = f"insert into ConsolidatedReport values\
                ({values_part})"
        self.db.cursor().execute(sql)
        self.db.commit()

class Insert_NonConsolidatedReport(InsertData):

    def get_html(self, html):
        if not html:
            return None
        return html.prettify()

    def operate(self, data):
        html = self.get_html(data.html)
        values_part = formatter().get_values_part(HtmlDC(rceptNo=data.rceptNo, html=html))
        sql = f"insert into NonConsolidatedReport values\
                ({values_part})"
        self.db.cursor().execute(sql)
        self.db.commit()


class formatter:

    def get_values_part(self, data):
        dic = data.dict()
        values = dic.values()

        values_part_lst = [self.get_string_format(value) for value in values]
        values_part = ', '.join(values_part_lst)
        return values_part


    def get_string_format(self, value):

        if type(value) == str:
            value = value.replace("'", "\'")
            value = value.replace('"', '\"')
            return f"'{value}'"

        elif type(value)==datetime:
            return f"'{value}'"

        elif value == None:
            return "Null"

        else:
            return f'{value}'