import re

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