from dataclasses import dataclass, asdict
import requests
from bs4 import BeautifulSoup
import time
import re
import random

class RandomSleep:

    def sleep(self):
        range_option = {'quicker': [0, .5], 'slower': [.5, 2], 'stop': [10, 15]}
        sleepLevel = random.choices(['quicker', 'slower', 'stop'], weights=[.6, .39, .01])
        range = range_option.get(sleepLevel[0])
        if sleepLevel[0] == 'stop' : print('Now taking a rest in a seconds')
        time.sleep(random.uniform(range[0], range[1]))

@dataclass
class ReportRequestParametersDC:
    text:str
    id:str
    rcpNo:str
    dcmNo:str
    eleId:str
    offset:str
    length:str
    dtd:str
    tocNo:str


class ReportRequestParametersNode2:      # the class to get detail parameter for request 'get' a report html in node2

    def __init__(self, reportHtml, parser):
        self.html = reportHtml
        self.parser = parser
        self.parameterKeyLst = ['text', 'id', 'rcpNo', 'dcmNo', 'eleId', 'offset', 'length', 'dtd', 'tocNo']    # detail parameters

    def get_parameterValue(self, key):
        return re.findall(r'node2\[\'' + key + '\'\]\s*=\s*(".*?")', self.html)  # search through the html to get the parser format string     ex. node2['text'] = "1. 회사의 개요"  <- get the part of ' " ... " '

    def get_all_parameters(self):

        parameterDic = {key : self.get_parameterValue(key) for key in self.parameterKeyLst}     #  {'text': ['"1. 회사의 개요"', '"2. 회사의 연혁"', ... ], 'id': ['"4"', '"5"', ...] ...}

        lst = []        # [{'text': '1. 회사의 개요', 'id': '4', ... 'tocNo': '4'}, ... ]
        for i in range(len(parameterDic.get('text'))) :
            dic = {key : parameterDic.get(key)[i].strip('"') for key in parameterDic.keys()}
            lst.append(dic)
        
        DCs = [ReportRequestParametersDC(**dic) for dic in lst]     # the list of dictionary to the list of dataclass.
        
        return DCs
    
    def get_report_parameters(self):        # get the node of a specific title such as "연결제무제표" or "제무재표 등"
        DCs = self.get_all_parameters()
        report_nord_parameter = [dc for dc in DCs if len(re.findall(self.parser, dc.text))>0]

        if report_nord_parameter :
            return report_nord_parameter
        
        return None
    

class ReportRequestParametersNode1:      # the class to get detail parameter for request 'get' a report html in node1

    def __init__(self, reportHtml, parser):
        self.html = reportHtml
        self.parser = parser
        self.parameterKeyLst = ['text', 'id', 'rcpNo', 'dcmNo', 'eleId', 'offset', 'length', 'dtd', 'tocNo']    # detail parameters

    def get_parameterValue(self, key):
        return re.findall(r'node1\[\'' + key + '\'\]\s*=\s*(".*?")', self.html)  # search through the html to get the parser format string     ex. node2['text'] = "1. 회사의 개요"  <- get the part of ' " ... " '

    def get_all_parameters(self):

        parameterDic = {key : self.get_parameterValue(key) for key in self.parameterKeyLst}     #  {'text': ['"1. 회사의 개요"', '"2. 회사의 연혁"', ... ], 'id': ['"4"', '"5"', ...] ...}

        lst = []        # [{'text': '1. 회사의 개요', 'id': '4', ... 'tocNo': '4'}, ... ]
        for i in range(len(parameterDic.get('text'))) :
            dic = {key : parameterDic.get(key)[i].strip('"') for key in parameterDic.keys()}
            lst.append(dic)
        
        DCs = [ReportRequestParametersDC(**dic) for dic in lst]     # the list of dictionary to the list of dataclass.
        return DCs
    
    def get_report_parameters(self):        # get the node of a specific title such as "연결제무제표" or "제무재표 등"
        DCs = self.get_all_parameters()
        report_nord_parameter = [dc for dc in DCs if len(re.findall(self.parser, dc.text))>0]

        if report_nord_parameter :
            return report_nord_parameter
        
        return None


class ReportRequestParametersHandler:

    def __init__(self, parser, successor=None):
        self.parser = parser
        self.successor = successor
        self.blackBox = ''

    def handle_request(self):
        reportRequestParameters = self.parser.get_report_parameters()
        if reportRequestParameters :
            self.blackBox += '\n' + '='*100 + '\n' + f'got the report params : \n {reportRequestParameters}'
            # print('='*100, f'got the report params : \n {reportRequestParameters}', sep='\n')
            return reportRequestParameters
        elif self.successor is not None:
            self.blackBox += '\n' + '='*100 + '\n' + 'now taked over successor'
            return self.successor.handle_request()
        else:
            # print('='*100, 'failed to get params : return None', sep='\n')
            self.blackBox += '\n' + '='*100 + '\n' + 'failed to get params : return None'
            return None

    def print_blackBox(self):
        print(self.blackBox)

class ReportRequestParametersProvider :

    def __init__(self, receptNo):
        self.receptNo = receptNo
        self.blackBox = ''

    def get_html(self, parser_format_1, parser_format_2):
        RandomSleep().sleep()
        url = f'http://dart.fss.or.kr/dsaf001/main.do?rcpNo={self.receptNo}'
        r = requests.get(url)
        reportHtml = r.text
        parser1 = ReportRequestParametersNode2(reportHtml, parser_format_1)
        parser2 = ReportRequestParametersNode1(reportHtml, parser_format_2)
        successor = ReportRequestParametersHandler(parser2)
        self.blackBox += successor.blackBox
        rrph = ReportRequestParametersHandler(parser1, successor)
        parameters = rrph.handle_request()
        self.blackBox += rrph.blackBox

        return parameters
    
    def print_blackBox(self):
        print(self.blackBox)

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
        

class ReportSearcher:
    # consolidatedParsers = [r'연\s*결\s*재\s*무\s*상\s*태\s*표\s*']
    # consolidatedParsers = [r'연\s*결\s*손\s*익\s*계\s*산\s*서\s*']
    # consolidatedParsers = [r'연\s*결\s*포\s*괄\s*손\s*익\s*계\s*산\s*서\s*']
    # consolidatedParsers = [r'연\s*결\s*현\s*금\s*흐\s*름\s*표']

    def __init__(self, html):
        self.html = html
        self.blackBox = ''

    def get_table(self, parser_format_lst):
        for p in self.html.find_all('p'):
            for parser in parser_format_lst:
                if re.findall(parser, p.get_text()):
                    # print('='*100, f'the p tag has the {parser} : \n {p}', sep='\n')
                    self.blackBox += '\n' + '='*100 + '\n' + f'the p tag has the {parser} : \n {p}'
                    tables = p.find_all_next('table')
                    return tables
        for td in self.html.find_all('td'):
            for parser in parser_format_lst:
                if re.findall(parser, td.get_text()):
                    # print('='*100, f'the td tag has the {parser} : \n {td}', sep='\n')
                    self.blackBox += '\n' + '='*100 + '\n' + f'the td tag has the {parser} : \n {td}'
                    tables = td.find_all_next('table')
                    return tables
        # print('='*100, f'fail to the title of the report : {parser_format_lst[0]} ext ... : None', sep='\n')
        self.blackBox += '\n' + '='*100 + '\n' + f'fail to the title of the report : {parser_format_lst[0]} ext ... : None'
        return None

    def print_blackBox(self):
        print(self.blackBox)
        

    
    # else:
    #     print(f"There's no data.")
    # for parser in parserLst:
    #     value = table_soup[0].find_all('p', re.compile(parser))
    #     print('='*100, value, sep='\n')

    # parser_format_1 = r'^[^가-힣]*재무제표$'
    # parser_format_2 = r'.*재무제표 등$'
    # nonConsolidatedParams = ReportRequestParametersProvider(receptNo).get_html(parser_format_1, parser_format_2)
    # html = ReportHtml().get_html(nonConsolidatedParams)
    # print('='*100, html, sep='\n')