import sys
from values import ValueSearcher

from pathlib import Path
import random
from rceptNoInfo import RceptnoInfo
import report
import parserFormat

from dataclasses import dataclass

@dataclass
class FundamentalDataDC:
    receptNo:str
    consolidatedEquity:int
    consolidatedliability:int
    consolidatedNetIncome:int
    consolidatedGrossProfit:int
    consolidatedOperatingProfit:int
    consolidatedConprehensiveNetIncome:int
    consolidatedConprehensiveGrossProfit:int
    consolidatedConprehensiveOperatingProfit:int
    consolidatedOperatingActivities:int

class FundamentalData:

    def __init__(self, receptNo):
        self.receptNo = receptNo
        self.blackBox = ''

    def get_data(self):
        parser_format_1 = r'.*연결재무제표$'
        parser_format_2 = r'.*재무제표 등$'
        
        rrpp = report.ReportRequestParametersProvider(self.receptNo)
        consolidatedParams = rrpp.get_html(parser_format_1, parser_format_2)
        self.blackBox += rrpp.blackBox
        rh = report.ReportHtml()
        html = rh.get_html(consolidatedParams)
        self.blackBox += rh.blackBox

        if html :

            rp = parserFormat.reportParserFormat()
            vp = parserFormat.valueParserFormat()

            parser_format_lst = rp.consolidated_balance_sheet
            rs = report.ReportSearcher(html)
            consolidated_balance_sheet = rs.get_table(parser_format_lst)
            self.blackBox += rs.blackBox

            if consolidated_balance_sheet:
                parserLst = vp.equity
                vs = ValueSearcher(consolidated_balance_sheet)
                consolidatedEquity = vs.get_values(parserLst)
                parserLst = vp.liability
                consolidatedliability = vs.get_values(parserLst)
                self.blackBox += vs.blackBox
            else :
                consolidatedEquity, consolidatedliability = None, None

            parser_format_lst = rp.consolidated_income_statement
            rs = report.ReportSearcher(html)
            consolidated_income_statement = rs.get_table(parser_format_lst)
            self.blackBox += rs.blackBox
            if consolidated_income_statement:
                parserLst = vp.netIncome
                vs = ValueSearcher(consolidated_income_statement)
                consolidatedNetIncome = vs.get_values(parserLst)
                parserLst = vp.grossProfit
                consolidatedGrossProfit = vs.get_values(parserLst)
                parserLst = vp.operatingProfit
                consolidatedOperatingProfit = vs.get_values(parserLst)
                self.blackBox += vs.blackBox
            else :
                consolidatedNetIncome, consolidatedGrossProfit, consolidatedOperatingProfit = None, None, None

            parser_format_lst = rp.consolidated_conprehensive_income_statement
            rs = report.ReportSearcher(html)
            consolidated_income_statement = rs.get_table(parser_format_lst)
            self.blackBox += rs.blackBox
            if consolidated_income_statement:
                parserLst = vp.netIncome
                vs = ValueSearcher(consolidated_income_statement)
                consolidatedConprehensiveNetIncome = vs.get_values(parserLst)
                parserLst = vp.grossProfit
                consolidatedConprehensiveGrossProfit = vs.get_values(parserLst)
                parserLst = vp.operatingProfit
                consolidatedConprehensiveOperatingProfit = vs.get_values(parserLst)
                self.blackBox += vs.blackBox
            else :
                consolidatedConprehensiveNetIncome, consolidatedConprehensiveGrossProfit, consolidatedConprehensiveOperatingProfit = None, None, None

            parser_format_lst = rp.consolidated_cash_flow_statement
            rs = report.ReportSearcher(html)
            consolidated_cash_flow_statement = rs.get_table(parser_format_lst)
            self.blackBox += rs.blackBox
            if consolidated_cash_flow_statement:
                parserLst = vp.operatingActivities
                vs = ValueSearcher(consolidated_cash_flow_statement)
                consolidatedOperatingActivities = vs.get_values(parserLst)
                self.blackBox += vs.blackBox
            else :
                consolidatedOperatingActivities = None
        
            return FundamentalDataDC(
                self.receptNo,
                consolidatedEquity,
                consolidatedliability,
                consolidatedNetIncome,
                consolidatedGrossProfit,
                consolidatedOperatingProfit,
                consolidatedConprehensiveNetIncome,
                consolidatedConprehensiveGrossProfit,
                consolidatedConprehensiveOperatingProfit,
                consolidatedOperatingActivities
        )
        else : 
            return FundamentalDataDC(self.receptNo, None, None, None, None, None, None, None, None, None)

    def print_blackBox(self):
        print(self.blackBox)

if __name__ == '__main__':

    import pandas as pd

    parentPath='c:/Users/ajcltm/PycharmProjects' # parent 경로
    sys.path.append(parentPath) # 경로 추가
    from DataAPI import stockInfo # from 다른 폴더(모듈) import 다른 파일

    path = Path.home().joinpath('Desktop', 'dataBackUp(211021)')

    stockList = pd.read_parquet(path/'stockListDB.parquet')
    tickers = stockList.ticker.unique().tolist()
    ticker = random.choice(tickers)
    commonStockProvider = stockInfo.commonStockProvider()
    stockinfo = stockInfo.StockInfo(path, commonStockProvider)
    stockInfoDic = stockinfo.get_stockInfo(ticker)
    corp_code = stockInfoDic[ticker]['corp_code']

    start = '20100101'
    end = '20211130'

    # ri = RceptnoInfo()
    # gen = ri.get_generator(corp_code, start, end)
    # lst = list(gen)
    # dc = random.choice(lst)
    # receptNo = dc.rcept_no


    
    print('\n'*4,'|', '>'*45,'Ajcltm', '<'*45,'|')

    # print('='*100, dc, sep='\n')

    receptNo = '20201116001840'
    # receptNo = '20100816001298'
    # receptNo = '20200928000281'
    # receptNo = '20180515001679'

    receptNos = ['20201116001840', '20100816001298', '20200928000281', '20180515001679']

    for receptNo in receptNos:
        fd = FundamentalData(receptNo)
        data = fd.get_data()
        # fd.print_blackBox()
        print('='*100, data, sep='\n')
    