parentPath='c:/Users/ajcltm/PycharmProjects/fundamentalData'
import sys
sys.path.append(parentPath)
from htmlScraper.nordParameter import ReportRequestParametersNode2, ReportRequestParametersNode1, ReportRequestParametersHandler

import requests
import time
import random
from fake_useragent import UserAgent

ua = UserAgent(use_cache_server=True)

class RandomSleep:

    def sleep(self):
        range_option = {'quicker': [0, .5], 'slower': [.5, 2], 'stop': [10, 15]}
        sleepLevel = random.choices(['quicker', 'slower', 'stop'], weights=[.6, .39, .01])
        range = range_option.get(sleepLevel[0])
        if sleepLevel[0] == 'stop' : print('Now taking a rest in a seconds')
        time.sleep(random.uniform(range[0], range[1]))

class ReportRequestParametersProvider :

    def __init__(self, receptNo):
        self.receptNo = receptNo
        self.blackBox = ''

    def get_html(self, parser_format_1, parser_format_2):
        RandomSleep().sleep()
        url = f'http://dart.fss.or.kr/dsaf001/main.do?rcpNo={self.receptNo}'
        r = requests.get(url, headers={'User-Agent' : str(ua.random)})
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