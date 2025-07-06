from pydantic import BaseModel
from typing import Optional, List

class LawCreate(BaseModel):
    name: str
    order_number: str
    adopted_date: str
    effective_date: str
    issuing_authority: str
    link: str

class LawResponse(LawCreate):
    id: int

class NormCreate(BaseModel):
    norm_name: str

class NormResponse(NormCreate):
    id: int

class NormGroupCreate(BaseModel):
    norm_id: int
    group_name: str

class NormGroupResponse(NormGroupCreate):
    id: int

class NormDocumentCreate(BaseModel):
    norm_id: int
    group_id: int
    code: str
    name: str
    link: str

class NormDocumentResponse(NormDocumentCreate):
    id: int

class StandardCreate(BaseModel):
    code: str
    name: str
    pdf_link: str

class StandardResponse(StandardCreate):
    id: int

class RegulationCreate(BaseModel):
    code: str
    name: str
    pdf_link: str

class RegulationResponse(RegulationCreate):
    id: int

class ResourceNormCreate(BaseModel):
    code: str
    name: str
    pdf_link: Optional[str] = None

class ResourceNormResponse(ResourceNormCreate):
    id: int

class ReferenceCreate(BaseModel):
    name: str
    pdf_link: str

class ReferenceResponse(ReferenceCreate):
    id: int