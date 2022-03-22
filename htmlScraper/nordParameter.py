from dataclasses import dataclass
import re


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
        
        
