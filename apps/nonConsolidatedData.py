parentPath='c:/Users/ajcltm/PycharmProjects/fundamentalData'
import sys
sys.path.append(parentPath)
from dartScraper.reportNordParameter import ReportRequestParametersProvider
from dartScraper.reportHtmlOfTables import ReportHtml
from htmlScraper.parserFormat import reportParserFormat, valueParserFormat
from htmlScraper.report import ReportSearcher
from htmlScraper.values import ValueSearcher
from pydantic import BaseModel
from typing import Optional, Any

import re

def get_unit(soup, parser_format_lst):
    unit_dic = {'원': 1, '천원':1000, '백만원': 1000000}

    for parser in parser_format_lst : 
        lst = soup.find_all(string=re.compile(parser))
        if lst :
            unit_string = lst[0].find_all_next(string=re.compile('단위'))[0]
            p = re.compile('[가-힣]*\s*원')
            unit_string = p.findall(unit_string)[0]
            unit_string = unit_string.replace(' ', '').replace(')', '').split(':')[-1]

            unit = unit_dic.get(unit_string)
            return unit
    unit = 1
    return unit

class HtmlDC(BaseModel):
    rceptNo:str
    html:Optional[Any]

class NonConsolidatedDataDC(BaseModel):
    rceptNo:str
    nonConsolidatedEquity:Optional[int]
    nonConsolidatedliability:Optional[int]
    nonConsolidatedNetIncome:Optional[int]
    nonConsolidatedGrossProfit:Optional[int]
    nonConsolidatedOperatingProfit:Optional[int]
    nonConsolidatedConprehensiveNetIncome:Optional[int]
    nonConsolidatedConprehensiveGrossProfit:Optional[int]
    nonConsolidatedConprehensiveOperatingProfit:Optional[int]
    nonConsolidatedOperatingActivities:Optional[int]

class NonConsolidatedData:

    def __init__(self, rceptNo):
        self.rceptNo = rceptNo
        self.html = None
        self.blackBox = ''

    def get_html(self, record = True):
        parser_format_1 = r'^[^가-힣]*재무제표$'
        parser_format_2 = r'.*재무제표 등$'
        rrpp = ReportRequestParametersProvider(self.rceptNo)
        consolidatedParams = rrpp.get_html(parser_format_1, parser_format_2)
        self.blackBox += rrpp.blackBox
        rh = ReportHtml()
        self.html = rh.get_html(consolidatedParams)
        if record == True:
            self.blackBox += rh.blackBox
        return HtmlDC(rceptNo=self.rceptNo, html=self.html)

    def get_data(self):

        html = self.get_html().html

        if html :

            rp = reportParserFormat()
            vp = valueParserFormat()

            parser_format_lst = rp.nonConsolidated_balance_sheet
            rs = ReportSearcher(html)
            nonConsolidated_balance_sheet = rs.get_table(parser_format_lst)
            self.blackBox += rs.blackBox

            if nonConsolidated_balance_sheet:
                unit = get_unit(html, parser_format_lst)

                vs = ValueSearcher(nonConsolidated_balance_sheet)

                parserLst = vp.equity
                value = vs.get_values(parserLst)
                if value : 
                    nonConsolidatedEquity = value * unit
                else :
                    nonConsolidatedEquity = None
                parserLst = vp.liability
                value = vs.get_values(parserLst)
                if value : 
                    nonConsolidatedliability = value * unit
                else :
                    nonConsolidatedliability = None
                self.blackBox += vs.blackBox
            else :
                nonConsolidatedEquity, nonConsolidatedliability = None, None

            parser_format_lst = rp.nonConsolidated_income_statement
            rs = ReportSearcher(html)
            nonConsolidated_income_statement = rs.get_table(parser_format_lst)
            self.blackBox += rs.blackBox
            if nonConsolidated_income_statement:
                unit = get_unit(html, parser_format_lst)

                vs = ValueSearcher(nonConsolidated_income_statement)

                parserLst = vp.netIncome
                value = vs.get_values(parserLst)
                if value : 
                    nonConsolidatedNetIncome = value * unit
                else :
                    nonConsolidatedNetIncome = None

                parserLst = vp.grossProfit
                value = vs.get_values(parserLst)
                if value : 
                    nonConsolidatedGrossProfit = value * unit
                else:
                    nonConsolidatedGrossProfit = None

                parserLst = vp.operatingProfit
                value = vs.get_values(parserLst)
                if value : 
                    nonConsolidatedOperatingProfit = value * unit
                else :
                    nonConsolidatedOperatingProfit = None
                    
                self.blackBox += vs.blackBox
            else :
                nonConsolidatedNetIncome, nonConsolidatedGrossProfit, nonConsolidatedOperatingProfit = None, None, None

            parser_format_lst = rp.nonConsolidated_conprehensive_income_statement
            rs = ReportSearcher(html)
            nonConsolidated_income_statement = rs.get_table(parser_format_lst)
            self.blackBox += rs.blackBox
            if nonConsolidated_income_statement:
                unit = get_unit(html, parser_format_lst)

                vs = ValueSearcher(nonConsolidated_income_statement)

                parserLst = vp.netIncome
                value = vs.get_values(parserLst)
                if value : 
                    nonConsolidatedConprehensiveNetIncome = value * unit
                else :
                    nonConsolidatedConprehensiveNetIncome = None
                parserLst = vp.grossProfit
                value = vs.get_values(parserLst)
                if value : 
                    nonConsolidatedConprehensiveGrossProfit = value * unit
                else :
                    nonConsolidatedConprehensiveGrossProfit = None
                parserLst = vp.operatingProfit
                value = vs.get_values(parserLst)
                if value : 
                    nonConsolidatedConprehensiveOperatingProfit = value * unit
                else :
                    nonConsolidatedConprehensiveOperatingProfit = None
                self.blackBox += vs.blackBox
            else :
                nonConsolidatedConprehensiveNetIncome, nonConsolidatedConprehensiveGrossProfit, nonConsolidatedConprehensiveOperatingProfit = None, None, None

            parser_format_lst = rp.nonConsolidated_cash_flow_statement
            rs = ReportSearcher(html)
            nonConsolidated_cash_flow_statement = rs.get_table(parser_format_lst)
            self.blackBox += rs.blackBox
            if nonConsolidated_cash_flow_statement:
                unit = get_unit(html, parser_format_lst)

                vs = ValueSearcher(nonConsolidated_cash_flow_statement)
                parserLst = vp.operatingActivities

                value = vs.get_values(parserLst)
                if value : 
                    nonConsolidatedOperatingActivities = value * unit
                else :
                    nonConsolidatedOperatingActivities = None
                self.blackBox += vs.blackBox
            else :
                nonConsolidatedOperatingActivities = None
        
            return NonConsolidatedDataDC(
                rceptNo=self.rceptNo,
                nonConsolidatedEquity=nonConsolidatedEquity,
                nonConsolidatedliability=nonConsolidatedliability,
                nonConsolidatedNetIncome=nonConsolidatedNetIncome,
                nonConsolidatedGrossProfit=nonConsolidatedGrossProfit,
                nonConsolidatedOperatingProfit=nonConsolidatedOperatingProfit,
                nonConsolidatedConprehensiveNetIncome=nonConsolidatedConprehensiveNetIncome,
                nonConsolidatedConprehensiveGrossProfit=nonConsolidatedConprehensiveGrossProfit,
                nonConsolidatedConprehensiveOperatingProfit=nonConsolidatedConprehensiveOperatingProfit,
                nonConsolidatedOperatingActivities=nonConsolidatedOperatingActivities
        )
        else : 
            return NonConsolidatedDataDC(rceptNo=self.rceptNo,
                nonConsolidatedEquity=None,
                nonConsolidatedliability=None,
                nonConsolidatedNetIncome=None,
                nonConsolidatedGrossProfit=None,
                nonConsolidatedOperatingProfit=None,
                nonConsolidatedConprehensiveNetIncome=None,
                nonConsolidatedConprehensiveGrossProfit=None,
                nonConsolidatedConprehensiveOperatingProfit=None,
                nonConsolidatedOperatingActivities=None
        )
    def print_blackBox(self):
        print(self.blackBox)

