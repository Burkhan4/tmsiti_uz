from pydantic import BaseModel
from typing import Optional
from fastapi import Form, File, UploadFile

class LawCreate(BaseModel):
    name: str
    order_number: str
    adopted_date: str
    effective_date: str
    issuing_authority: str
    link: str

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        order_number: str = Form(...),
        adopted_date: str = Form(...),
        effective_date: str = Form(...),
        issuing_authority: str = Form(...),
        link: UploadFile = File(...)
    ):
        return cls(
            name=name,
            order_number=order_number,
            adopted_date=adopted_date,
            effective_date=effective_date,
            issuing_authority=issuing_authority,
            link=link
        )

class LawResponse(LawCreate):
    id: int

class UrbanNormCreate(BaseModel):
    norm_name: str

class UrbanNormResponse(UrbanNormCreate):
    id: int

class NormGroupCreate(BaseModel):
    group_name: str

class NormGroupResponse(NormGroupCreate):
    id: int
    norm_id: int

class NormDocumentCreate(BaseModel):
    code: str
    name: str
    link: str

    @classmethod
    def as_form(
        cls,
        code: str = Form(...),
        name: str = Form(...),
        link: UploadFile = File(...)
    ):
        return cls(code=code, name=name, link=link)

class NormDocumentResponse(NormDocumentCreate):
    id: int
    norm_id: int
    group_id: int

class StandardCreate(BaseModel):
    code: str
    name: str
    pdf_link: str

    @classmethod
    def as_form(
        cls,
        code: str = Form(...),
        name: str = Form(...),
        pdf_link: UploadFile = File(...)
    ):
        return cls(code=code, name=name, pdf_link=pdf_link)

class StandardResponse(StandardCreate):
    id: int

class RegulationCreate(BaseModel):
    code: str
    name: str
    pdf_link: str

    @classmethod
    def as_form(
        cls,
        code: str = Form(...),
        name: str = Form(...),
        pdf_link: UploadFile = File(...)
    ):
        return cls(code=code, name=name, pdf_link=pdf_link)

class RegulationResponse(RegulationCreate):
    id: int

class ResourceNormCreate(BaseModel):
    code: str
    name: str
    pdf_link: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        code: str = Form(...),
        name: str = Form(...),
        pdf_link: UploadFile = File(None)
    ):
        return cls(code=code, name=name, pdf_link=pdf_link)

class ResourceNormResponse(ResourceNormCreate):
    id: int

class ReferenceDocCreate(BaseModel):
    name: str
    pdf_link: str

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        pdf_link: UploadFile = File(...)
    ):
        return cls(name=name, pdf_link=pdf_link)

class ReferenceDocResponse(ReferenceDocCreate):
    id: int