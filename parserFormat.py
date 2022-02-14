from dataclasses import dataclass, field

@dataclass
class reportParserFormat:
    consolidated_balance_sheet : list() = field(default_factory=list)
    consolidated_income_statement : list() = field(default_factory=list)
    consolidatedNetIncome : list() = field(default_factory=list)
    consolidated_cash_flow_statement : list() = field(default_factory=list)

    nonConsolidated_balance_sheet : list() = field(default_factory=list)
    nonConsolidated_income_statement : list() = field(default_factory=list)
    nonConsolidatedNetIncome : list() = field(default_factory=list)
    nonConsolidated_cash_flow_statement : list() = field(default_factory=list)

    def __post_init__(self):
        self.consolidated_balance_sheet = [r'연\s*결\s*재\s*무\s*상\s*태\s*표\s*', r'연\s*결\s*대\s*차\s*대\s*조\s*표\s*']
        self.consolidated_income_statement = [r'연\s*결\s*손\s*익\s*계\s*산\s*서\s*']
        self.consolidated_conprehensive_income_statement = [r'연\s*결\s포\s*괄\s*손\s*익\s*계\s*산\s*서\s*', r'연.*결.포.*괄.*손.*익.*계.*산.*서.*'] #r'포.*괄.*'
        self.consolidated_cash_flow_statement = [r'연\s*결\s*현\s*금\s*흐\s*름\s*표\s*']

        self.nonConsolidated_balance_sheet : list() = [r'^[^가-힣]*재\s*무\s*상\s*태\s*표\s*', r'^[가나다라마바사아]*[^가-힣]*재\s*무\s*상\s*태\s*표\s*', r'^[^가-힣]*대\s*차\s*대\s*조\s*표\s*']
        self.nonConsolidated_income_statement : list() = [r'^[^가-힣]*손\s*익\s*계\s*산\s*서\s*', r'^[가나다라마바사아]*[^가-힣]*손\s*익\s*계\s*산\s*서\s*']
        self.nonConsolidated_conprehensive_income_statement : list() = [r'^[^가-힣]*포\s*괄\s*손\s*익\s*계\s*산\s*서\s*', r'^[가나다라마바사아]*[^가-힣]*포\s*괄\s*손\s*익\s*계\s*산\s*서\s*']
        self.nonConsolidated_cash_flow_statement : list() = [r'^[^가-힣]*현\s*금\s*흐\s*름\s*표\s*', r'^[가나다라마바사아]*[^가-힣]*현\s*금\s*흐\s*름\s*표\s*']


@dataclass
class valueParserFormat:

    equity : list() = field(default_factory=list)
    liability : list() = field(default_factory=list)

    netIncome : list() = field(default_factory=list)
    grossProfit : list() = field(default_factory=list)
    operatingProfit : list() = field(default_factory=list)
    
    operatingActivities : list() = field(default_factory=list)

    def __post_init__(self):
        self.equity = [r'^자본총계$',r'^[^가-힣]*자\s*본\s*총\s*계\s*', r'^[가나다라마바사아]*[^가-힣]*자\s*본\s*총\s*계\s*']
        self.liability = [r'^부채총계$',r'^[^가-힣]*부\s*채\s*총\s*계\s*', r'^[가나다라마바사아]*[^가-힣]*부\s*채\s*총\s*계\s*']

        self.netIncome = [r'^당\s*기\s*순\s*이\s*익\s*', r'^[^가-힣]*당\s*기\s*순\s*이\s*익\s*', r'^[가나다라마바사아]*[^가-힣]*당\s*기\s*순\s*이\s*익\s*',
                    r'^당\s*기\s*연\s*결\s*순\s*이\s*익\s*', r'^[^가-힣]*당\s*기\s*연\s*결\s*순\s*이\s*익\s*', r'^[가나다라마바사아]*[^가-힣]*당\s*기\s*연\s*결\s*순\s*이\s*익\s*',
                    r'^반\s*기\s*순\s*이\s*익\s*', r'^[^가-힣]*반\s*기\s*순\s*이\s*익\s*', r'^[가나다라마바사아]*[^가-힣]*반\s*기\s*순\s*이\s*익\s*',
                    r'^반\s*기\s*연\s*결\s*순\s*이\s*익\s*', r'^[^가-힣]*반\s*기\s*연\s*결\s*순\s*이\s*익\s*', r'^[가나다라마바사아]*[^가-힣]*반\s*기\s*연\s*결\s*순\s*이\s*익\s*',
                    r'^분\s*기\s*순\s*이\s*익\s*', r'^[^가-힣]*분\s*기\s*순\s*이\s*익\s*', r'^[가나다라마바사아]*[^가-힣]*분\s*기\s*순\s*이\s*익\s*', r'[^계중].*기.*순.*이.*익',
                    r'^분\s*기\s*연\s*결\s*순\s*이\s*익\s*', r'^[^가-힣]*분\s*기\s*연\s*결\s*순\s*이\s*익\s*', r'^[가나다라마바사아]*[^가-힣]*분\s*기\s*연\s*결\s*순\s*이\s*익\s*',
                    r'^당\s분\s*기\s*[연\s*결\s]*순\s*이\s*익\s*', r'^[^가-힣]*당\s*분\s*기\s*[연\s*결\s]*순\s*이\s*익\s*', r'^[가나다라마바사아]*[^가-힣]*당\s*분\s*기\s*[연\s*결\s]*순\s*이\s*익\s*']
        self.grossProfit = [r'매\s*출\s*총\s*이\s*익\s*',r'[^가-힣]*매\s*출\s*총\s*이\s*익\s*', r'^[가나다라마바사아]*[^가-힣]*매\s*출\s*총\s*이\s*익\s*']
        self.operatingProfit = [r'영\s*업\s*이\s*익\s*',r'^[^가-힣]*영\s*업\s*이\s*익\s*', r'^[가나다라마바사아]*[^가-힣]*영\s*업\s*이\s*익\s*']

        self.operatingActivities = [r'영\s*업\s*활\s*동\s*현\s*금\s*흐\s*름', r'^[^가-힣]*영\s*업\s*활\s*동\s*현\s*금\s*흐\s*름\s*', r'^[가나다라마바사아]*[^가-힣]*영\s*업\s*활\s*동\s*현\s*금\s*흐\s*름\s*',
                                          r'영.*업.*활.*동.*현.*금.*흐.*름.*',
                                          r'영.*업.*활.*동.*으.*로.*부.*터.*의.*현.*금.*흐.*름.*', r'영.*업.*활.*동.*으.*로.*인.*한.*현.*금.*흐.*름.*']

