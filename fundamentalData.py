import sys
from values import ValueSearcher

from pathlib import Path
import random
import report
import parserFormat
import consolidatedData
import nonConsolidatedData

from dataclasses import dataclass


import pandas as pd


class FundamentalData:

    def __init__(self, receptNo):
        self.cfd = consolidatedData.ConsolidatedData(receptNo)
        self.ncfd = nonConsolidatedData.NonConsolidatedData(receptNo)
        self.blackBox = ""

        self.consolidatedData = self.get_consolidatedData()
        self.nonConsolidatedData = self.get_nonConsolidatedData()
        self.consolidatedHtml = self.get_consolidatedHtml()
        self.nonConsolidatedHtml = self.get_nonConsolidatedHtml()

    def get_consolidatedData(self):

        data = self.cfd.get_data()
        self.blackBox += self.cfd.blackBox

        return data

    def get_nonConsolidatedData(self):

        data = self.ncfd.get_data()
        self.blackBox += self.ncfd.blackBox

        return data

    def get_consolidatedHtml(self):
        html = self.cfd.get_html(record=False)

        return html

    def get_nonConsolidatedHtml(self):
        html = self.ncfd.get_html(record=False)

        return html

    def print_blackBox(self):
        print(self.blackBox)


if __name__=='__main__':

    # parentPath='c:/Users/ajcltm/PycharmProjects' # parent 경로
    # sys.path.append(parentPath) # 경로 추가
    # from DataAPI import stockInfo # from 다른 폴더(모듈) import 다른 파일

    # path = Path.home().joinpath('Desktop', 'dataBackUp(211021)')

    # stockList = pd.read_parquet(path/'stockListDB.parquet')
    # tickers = stockList.ticker.unique().tolist()
    # ticker = random.choice(tickers)
    # commonStockProvider = stockInfo.commonStockProvider()
    # stockinfo = stockInfo.StockInfo(path, commonStockProvider)
    # stockInfoDic = stockinfo.get_stockInfo(ticker)
    # corp_code = stockInfoDic[ticker]['corp_code']

    # start = '20100101'
    # end = '20211130'

    # ri = RceptNoInfoProvider()
    # gen = ri.get_generator(corp_code, start, end)
    # lst = list(gen)
    # dc = random.choice(lst)
    # rceptNo = dc.rcept_no


    
    print('\n'*4,'|', '>'*45,'Ajcltm', '<'*45,'|')

    # print('='*100, dc, sep='\n')

    # rceptNo = '20201116001840'
    # rceptNo = '20100816001298'
    # rceptNo = '20200928000281'
    # rceptNo = '20180515001679'

    rceptNos = ['20201116001840', '20100816001298', '20200928000281', '20180515001679']

    for rceptNo in rceptNos:
        fd = FundamentalData(rceptNo)
        print(fd.blackBox)
        print(fd.consolidatedData)
        print(fd.nonConsolidatedData)


