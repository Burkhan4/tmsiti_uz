from pydantic import BaseModel
from typing import Optional, List

class Law(BaseModel):
    name: str
    order_number: str
    adopted_date: str
    effective_date: str
    issuing_authority: str
    link: str

class Norm(BaseModel):
    norm_name: str

class NormGroup(BaseModel):
    norm_id: int
    group_name: str

class NormDocument(BaseModel):
    norm_id: int
    group_id: int
    code: str
    name: str
    link: str

class Standard(BaseModel):
    code: str
    name: str
    pdf_link: str

class Regulation(BaseModel):
    code: str
    name: str
    pdf_link: str

class ResourceNorm(BaseModel):
    code: str
    name: str
    pdf_link: Optional[str] = None

class Reference(BaseModel):
    name: str
    pdf_link: str