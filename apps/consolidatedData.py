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

class ConsolidatedDataDC(BaseModel):
    rceptNo:str
    consolidatedEquity:Optional[int]
    consolidatedliability:Optional[int]
    consolidatedNetIncome:Optional[int]
    consolidatedGrossProfit:Optional[int]
    consolidatedOperatingProfit:Optional[int]
    consolidatedConprehensiveNetIncome:Optional[int]
    consolidatedConprehensiveGrossProfit:Optional[int]
    consolidatedConprehensiveOperatingProfit:Optional[int]
    consolidatedOperatingActivities:Optional[int]

class ConsolidatedData:

    def __init__(self, rceptNo):
        self.rceptNo = rceptNo
        self.html = None
        self.blackBox = ''

    def get_html(self, record = True):
        parser_format_1 = r'.*연결재무제표$'
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

            parser_format_lst = rp.consolidated_balance_sheet
            rs = ReportSearcher(html)
            consolidated_balance_sheet = rs.get_table(parser_format_lst)
            self.blackBox += rs.blackBox

            if consolidated_balance_sheet:
                unit = get_unit(html, parser_format_lst)

                vs = ValueSearcher(consolidated_balance_sheet)

                parserLst = vp.equity
                value = vs.get_values(parserLst)
                if value :
                    consolidatedEquity = value * unit
                else : 
                    consolidatedEquity = None

                parserLst = vp.liability
                value = vs.get_values(parserLst)
                if value :
                    consolidatedliability = value * unit
                else : 
                    consolidatedliability = None
                self.blackBox += vs.blackBox
            else :
                consolidatedEquity, consolidatedliability = None, None

            parser_format_lst = rp.consolidated_income_statement
            rs = ReportSearcher(html)
            consolidated_income_statement = rs.get_table(parser_format_lst)
            self.blackBox += rs.blackBox
            if consolidated_income_statement:
                
                vs = ValueSearcher(consolidated_income_statement)

                parserLst = vp.netIncome
                value = vs.get_values(parserLst)
                if value :
                    consolidatedNetIncome = value * unit
                else : 
                    consolidatedNetIncome = None

                parserLst = vp.grossProfit
                value = vs.get_values(parserLst)
                if value :
                    consolidatedGrossProfit = value * unit
                else : 
                    consolidatedGrossProfit = None

                parserLst = vp.operatingProfit
                value = vs.get_values(parserLst)
                if value :
                    consolidatedOperatingProfit = value * unit
                else : 
                    consolidatedOperatingProfit = None
                self.blackBox += vs.blackBox
            else :
                consolidatedNetIncome, consolidatedGrossProfit, consolidatedOperatingProfit = None, None, None

            parser_format_lst = rp.consolidated_conprehensive_income_statement
            rs = ReportSearcher(html)
            consolidated_income_statement = rs.get_table(parser_format_lst)
            self.blackBox += rs.blackBox
            if consolidated_income_statement:
                
                vs = ValueSearcher(consolidated_income_statement)

                parserLst = vp.netIncome
                value = vs.get_values(parserLst)
                if value :
                    consolidatedConprehensiveNetIncome = value * unit
                else : 
                    consolidatedConprehensiveNetIncome = None

                parserLst = vp.grossProfit
                value = vs.get_values(parserLst)
                if value :
                    consolidatedConprehensiveGrossProfit = value * unit
                else : 
                    consolidatedConprehensiveGrossProfit = None

                parserLst = vp.operatingProfit
                value = vs.get_values(parserLst)
                if value :
                    consolidatedConprehensiveOperatingProfit = value * unit
                else : 
                    consolidatedConprehensiveOperatingProfit = None

                self.blackBox += vs.blackBox
            else :
                consolidatedConprehensiveNetIncome, consolidatedConprehensiveGrossProfit, consolidatedConprehensiveOperatingProfit = None, None, None

            parser_format_lst = rp.consolidated_cash_flow_statement
            rs = ReportSearcher(html)
            consolidated_cash_flow_statement = rs.get_table(parser_format_lst)
            self.blackBox += rs.blackBox
            if consolidated_cash_flow_statement:
                
                vs = ValueSearcher(consolidated_cash_flow_statement)

                parserLst = vp.operatingActivities
                value = vs.get_values(parserLst)
                if value :
                    consolidatedOperatingActivities = value * unit
                else : 
                    consolidatedOperatingActivities = None
                    
                self.blackBox += vs.blackBox
            else :
                consolidatedOperatingActivities = None
        
            return ConsolidatedDataDC(
                rceptNo=self.rceptNo,
                consolidatedEquity=consolidatedEquity,
                consolidatedliability=consolidatedliability,
                consolidatedNetIncome=consolidatedNetIncome,
                consolidatedGrossProfit=consolidatedGrossProfit,
                consolidatedOperatingProfit=consolidatedOperatingProfit,
                consolidatedConprehensiveNetIncome=consolidatedConprehensiveNetIncome,
                consolidatedConprehensiveGrossProfit=consolidatedConprehensiveGrossProfit,
                consolidatedConprehensiveOperatingProfit=consolidatedConprehensiveOperatingProfit,
                consolidatedOperatingActivities=consolidatedOperatingActivities
                )
        else : 
            return ConsolidatedDataDC(
                rceptNo=self.rceptNo,
                consolidatedEquity=None,
                consolidatedliability=None,
                consolidatedNetIncome=None,
                consolidatedGrossProfit=None,
                consolidatedOperatingProfit=None,
                consolidatedConprehensiveNetIncome=None,
                consolidatedConprehensiveGrossProfit=None,
                consolidatedConprehensiveOperatingProfit=None,
                consolidatedOperatingActivities=None
            )
    def print_blackBox(self):
        print(self.blackBox)
    