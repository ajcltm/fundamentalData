import abc
from dataclasses import dataclass, field
import re
import requests



class Handler(metaclass=abc.ABCMeta):       # abstract class to handle json result (consists of requester and successor)

    def __init__(self,  requester, successor=None):
        self._requester = requester     # the requester which try to get json
        self._successor = successor     # the successor which is operated in case that the result of the requester is failed to meet a certain condition
        
    @abc.abstractmethod
    def handle_request(self):       # the trigger method (This is a abstractmethod)
        pass


class jsonHandler(Handler):     # the concreteHandler inherits the class 'Handler' (include '__init__' method and initial variaces)

    def handle_request(self):
        r = self._requester.operation()

        if r.json()['status'] == '000':     # if the json result is '000', the proccess is completed.
            return r.json()['list']
        elif self._successor is not None:   # if the json result is not '000', take over the proccess to the successor.
            self._successor.handle_request()
        else :
            return None


class RequesterAF(abc.ABC):     # abstract class for url requesters
    """This is the interface which requests rceptNo information (concrete functions would be a document version of 'A'or 'F')"""
    
    @abc.abstractmethod
    def operation(self, documentVersion):   # documentVersion consists of 'A' and 'F' (A: 사업보고서 / F: 감사보고서)
        pass


class RequesterA(RequesterAF):      # url requester to get recptNoInfo which of documentVersion is 'A' (the type is json)
    """A concrete function that requests rceptNo. pblntf_ty is 'A'"""
    documentVersion = 'A'
    url = 'https://opendart.fss.or.kr/api/list.json'
    paramsDict = None

    def __init__(self, corp_code, start, end):
        self.paramsDict = {
            'crtfc_key' : '92c176817e681dcc4ad263eb3fa5182792b0b7a3',
            'corp_code' : corp_code,
            'bgn_de' : start,
            'end_de' : end,
            'pblntf_ty': self.documentVersion,
            'last_reprt_at' : 'N',
            'page_count' : 100
        }
    
    def operation(self):
        return requests.get(self.url, self.paramsDict)


class RequesterF(RequesterAF):      # url requester to get recptNoInfo which of documentVersion is 'F' (the type is json)
    """A concrete function that requests rceptNo. pblntf_ty is 'F'"""
    documentVersion = 'F'
    url = 'https://opendart.fss.or.kr/api/list.json'
    paramsDict = None

    def __init__(self, corp_code, start, end):
        self.paramsDict = {
            'crtfc_key' : '92c176817e681dcc4ad263eb3fa5182792b0b7a3',
            'corp_code' : corp_code,
            'bgn_de' : start,
            'end_de' : end,
            'pblntf_ty': self.documentVersion,
            'last_reprt_at' : 'N',
            'page_count' : 100
        }
    
    def operation(self):
        return requests.get(self.url, self.paramsDict)

@dataclass      # RepctNoInfo dataclass
class RepctNoInfo:
    corp_code:str       # ex. '00126380'
    corp_name:str       # ex. '삼성전자'
    stock_code:str      # ex. '005930'
    corp_cls:str        # ex. 'Y'
    report_nm:str       # ex. '반기보고서 (2021.06)'
    rcept_no:str        # ex. '20210817001416'
    flr_nm:str          # ex. '삼성전자'
    rcept_dt:str        # ex. '20210817'
    rm:str              # ex. '연'
    add_info:str=field(default=None)    # created by __post_init__  , ex. '첨부추가'
    kind:str=field(default=None)    # created by __post_init__ , ex. '사업보고서', or '분기보고서' etc
    date:str=field(default=None)    # created by __post_init__ , ex. '2009.12'

    def __post_init__(self):
        parser = r'\[?(\w*)\]?(사업보고서|반기보고서|분기보고서|감사보고서|연결감사보고서).*\((\d{4}\.\d{2})\)'
        # var parser is divided into 3 group which are (\w*), (사업보고서|반기보고서|...) and (\d{4}\.\d{2}). (respectively add_info, kind and date)
        re_lst = re.findall(parser, self.report_nm)[0]      # re_lst like... -> [('', '분기보고서', '2010.09')]
        self.add_info = re_lst[0]
        self.kind = re_lst[1]
        self.date = re_lst[2]

class RceptnoInfo:      # client class

    def get_generator(self, corp_code, start, end) :

        requesterA = RequesterA(corp_code, start, end)  # try the first A requester (to get recetpNoInfo for documentVersion 'A(사업보고서)')
        requesterF = RequesterF(corp_code, start, end)  # try the second F requester (to get recetpNoInfo for documentVersion 'F(감사보고서)')
        successor = jsonHandler(requesterF)     # the second handler which dosen't have a successor (that means the last handler)
        result = jsonHandler(requesterA, successor).handle_request()        # the first handler which has a successor handler
        gen = (RepctNoInfo(**i) for i in result)    # comprehension to get a generator. ex. (dataclass1, dataclass2, ... , dataclass_n )

        return gen


if __name__ == '__main__':

    corp_code = '005930'
    start = '20100101'
    end = '20211130'

    ri = RceptnoInfo()
    gen = ri.get_generator(corp_code, start, end)

    for i in enumerate(gen):
        if i[0] == 2:
            break
        print('='*100, f'{i[1]}', sep='\n')
