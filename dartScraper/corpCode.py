parentPath='c:/Users/ajcltm/PycharmProjects/fundamentalData'
import sys
sys.path.append(parentPath)
from dartScraper.models import CorpCodeDC

from pathlib import Path
from zipfile import ZipFile
from io import BytesIO

import requests
from xml.etree.ElementTree import parse


class CorpCodeScraper:

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
        dcs = [CorpCodeDC(corp_code = x.findtext("corp_code"), 
                        corp_name = x.findtext("corp_name"), 
                        stock_code = x.findtext("stock_code"), 
                        modify_date = x.findtext("modify_date")) for x in list]

        return dcs