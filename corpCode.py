from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from dataclasses import dataclass
import requests
from xml.etree.ElementTree import parse
import sqlite3
from tqdm import tqdm

@dataclass
class CorpCodeDC:
    corpCode:str
    corpName:str
    stockCode:str
    modifyDate:str

    def __post_init__(self):
        if self.corpCode == ' ':
            self.corpCode = None
        if self.corpCode :
            self.corpCode = self.corpCode.replace("'", '')
        if self.corpName == ' ':
            self.corpName = None
        if self.corpName :
            self.corpName = self.corpName.replace("'", '')
        if self.stockCode == ' ':
            self.stockCode = None
        if self.stockCode :
            self.stockCode = self.stockCode.replace("'", '')
        if self.modifyDate == ' ':
            self.modifyDate = None
        if self.modifyDate :
            self.modifyDate = self.modifyDate.replace("'", '')


class CorpCode:

    def __init__(self):
        self.url = 'https://opendart.fss.or.kr/api/corpCode.xml'
        self.params = {'crtfc_key' : '92c176817e681dcc4ad263eb3fa5182792b0b7a3'}
        self.dir = Path.cwd().joinpath('fundamentalData','db')

    def get_requests(self):

        r = requests.get(self.url, self.params)

        return r

    def downloadXmlFile(self):
        r = self.get_requests()
        z = ZipFile(BytesIO(r.content))
        z.extractall(self.dir)

    def get_dcs(self):

        tree = parse(self.dir/'CORPCODE.xml')
        root = tree.getroot()
        list = root.findall("list")
        dcs = [CorpCodeDC(x.findtext("corp_code"),x.findtext("corp_name"),x.findtext("stock_code"), x.findtext("modify_date")) for x in list]

        return dcs

    def create_db(self):
        dbFile = self.dir / 'corpCode.db'
        con = sqlite3.connect(dbFile)
        cur = con.cursor()

        query = 'CREATE TABLE corpCodeInfo (corpCode TEXT, corpName TEXT, stockCode TEXT, modifyDate TEXT)'
        cur.execute(query)
        con.commit()

        dcs = self.get_dcs()

        for dc in tqdm(dcs, bar_format='{l_bar}{bar:20}{r_bar}{bar:-20b}'):
        # for dc in dcs:
            values = f"('{dc.corpCode}', '{dc.corpName}', '{dc.stockCode}', '{dc.modifyDate}')"
            # print(values)
            query = f'INSERT INTO corpCodeInfo VALUES {values}'
            cur.execute(query)
            con.commit()
        
        con.close()


if __name__ == '__main__':
    cc = CorpCode()
    cc.downloadXmlFile()
    cc.create_db()
    # print(cc.get_dcs()[0])