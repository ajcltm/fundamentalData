from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CorpCodeData(BaseModel):
    corp_code: Optional[str]
    corp_name: Optional[str]
    stock_code: Optional[str]
    modify_date: Optional[datetime]

class RceptNoInfo(BaseModel):
    corp_code:str       # ex. '00126380'
    corp_name:str       # ex. '삼성전자'
    stock_code:str      # ex. '005930'
    corp_cls:str        # ex. 'Y'
    report_nm:str       # ex. '반기보고서 (2021.06)'
    rcept_no:str        # ex. '20210817001416'
    flr_nm:str          # ex. '삼성전자'
    rcept_dt:str        # ex. '20210817'
    rm:str              # ex. '연'
    add_info:Optional[str]    # created by __post_init__  , ex. '첨부추가'
    kind:Optional[str]   # created by __post_init__ , ex. '사업보고서', or '분기보고서' etc
    date:Optional[datetime]    # created by __post_init__ , ex. '2009.12'

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

class HtmlDC(BaseModel):
    rceptNo:str
    html:Optional[str]

