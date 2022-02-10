import abc
from dataclasses import dataclass, asdict
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import re

from parserFormat import reportParserFormat, valueParserFormat


@dataclass
class FundamentalValues:
    consolidatedEquity:int
    consolidatedLiability:int
    consolidatedNetIncome:int
    consolidatedGrossProfit:int
    consolidatedOperatingProfit:int
    consolidatedComprehensiveNetIncome:int
    consolidatedComprehensiveGrossProfit:int
    consolidatedComprehensiveOperatingProfit:int
    consolidatedOperatingActivities:int

    equity:int
    liability:int
    netIncome:int
    grossProfit:int
    operatingProfit:int
    comprehensiveNetIncome:int
    comprehensiveGrossProfit:int
    comprehensiveOperatingProfit:int
    operatingActivities:int


class ValueSearcher:

    def __init__(self, table_soup):
        self.table_soup = table_soup

        self.findedParser = None


    def get_values(self, parser_format_lst):
        for table in self.table_soup:
            tr_tags = table.find_all('tr')
            target_tr_tag = self.find_target_tr_tag(tr_tags, parser_format_lst)
            if target_tr_tag:
                numeric = self.get_numeric(target_tr_tag)
                if numeric:
                    print('='*100, f'numeric : {numeric}', sep='\n')
                    value = int(numeric.replace(',', ''))
                    print('='*100, f'{self.findedParser} : {value}', sep='\n')
                    return value
        print('='*100, f'{parser_format_lst[0]} ext... : None', sep='\n')
        return None


    def find_target_tr_tag(self, tr_tags, parser_format_lst):
        for tr_tag in tr_tags:
            text = tr_tag.get_text()
            for parser in parser_format_lst:
                if re.findall(parser, text):
                    # print(f'got the value tr_tag {tr_tag}')
                    self.findedParser = parser
                    return tr_tag
        return None

    def get_numeric(self, tr_tag):
        descendants = tr_tag.children
        for d in descendants:
            try:
                text = d.get_text()
                print(text)
                if re.findall(r'\<.*\>([0-9]+)', text):
                    return d.contents[0]
            except:
                pass
        return None