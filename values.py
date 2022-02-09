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

    def get_value(self, parser_format_lst):
        tr_tags = self.table_soup[0].find_all('tr')
        target_tr_tag = self.find_target_tr(tr_tags, parser_format_lst)
        if target_tr_tag :
            numeric_tr_p = self.get_numeric_tr_p_tags(target_tr_tag)
            text = numeric_tr_p.get_text().strip()
            value = int(text.replace(',', ''))
            print('='*100, f'{self.findedParser} : {value}', sep='\n')
            return value
        print(f'{parser_format_lst} : value is not found')
        return None

    def find_target_tr(self, tr_tags, parser_format_lst):
        for tr in tr_tags:
            tr_p_tags = tr.find_all('p')
            if self.find_target_tr_p(tr_p_tags, parser_format_lst):
                return tr
            
    def find_target_tr_p(self, tr_p_tags, parser_format_lst):
        for parser in parser_format_lst:
            for tr_p_tag in tr_p_tags:
                text = tr_p_tag.get_text().strip()
                if re.findall(parser, text):
                    self.findedParser = parser
                    return True

    def get_numeric_tr_p_tags(self, tr_tags):
        tr_p_tags = tr_tags.find_all('p')
        for tr_p_tag in tr_p_tags:
            text = tr_p_tag.get_text().strip()
            if re.findall(r'[0-9]+', text):
                return tr_p_tag