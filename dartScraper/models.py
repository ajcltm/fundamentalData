from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class CorpCodeDC(BaseModel):
    corp_code: Optional[str]
    corp_name: Optional[str]
    stock_code: Optional[str]
    modify_date: Optional[datetime]

    @validator('corp_code', 'corp_name', 'stock_code', pre=True, always=True)
    def dealWithComma(cls, v):
        if v == ' ':
            return None
        if v :
            return v.replace("'", '')

    @validator('modify_date', pre=True, always=True)
    def to_datetime(cls, v):
        if v == ' ':
            return None
        if v :
            return  datetime.strptime(v.replace("'", ''), '%Y%m%d')