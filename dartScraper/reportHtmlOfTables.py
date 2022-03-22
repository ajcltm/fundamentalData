from dataclasses import asdict
import requests
from bs4 import BeautifulSoup

class ReportHtml :
    blackBox = ''

    def get_html(self, detailReportParameter):
        url = f'http://dart.fss.or.kr/report/viewer.do?'
        r = requests.get(url, params=asdict(detailReportParameter[0]))
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find_all('table')
        if table :
            # print('='*100,'success to get the table with those params', sep='\n')
            self.blackBox += '\n' + '='*100 + '\n' + f'success to get the table with those params'
            return soup
        else:
            # print('='*100, 'fail to get the report with those params : None', sep='\n')
            self.blackBox += '\n' + '='*100 + '\n' + f'fail to get the report with those params : None'
            return None
    
    def print_blackBox(self):
        print(self.blackBox)