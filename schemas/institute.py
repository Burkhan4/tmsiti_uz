from pydantic import BaseModel
from typing import Optional
from fastapi import Form, File, UploadFile

class InstituteInfoCreate(BaseModel):
    content: str
    charter_pdf: Optional[str] = None
    statute_pdf: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        content: str = Form(...),
        charter_pdf: UploadFile = File(None),
        statute_pdf: UploadFile = File(None)
    ):
        return cls(content=content, charter_pdf=charter_pdf, statute_pdf=statute_pdf)

class InstituteInfoResponse(InstituteInfoCreate):
    id: int

class ManagementCreate(BaseModel):
    image: Optional[str] = None
    position: str
    full_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    specialty: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        image: UploadFile = File(None),
        position: str = Form(...),
        full_name: str = Form(...),
        phone: str = Form(None),
        email: str = Form(None),
        specialty: str = Form(None)
    ):
        return cls(image=image, position=position, full_name=full_name, phone=phone, email=email, specialty=specialty)

class ManagementResponse(ManagementCreate):
    id: int

class StructureCreate(BaseModel):
    image: str

    @classmethod
    def as_form(cls, image: UploadFile = File(...)):
        return cls(image=image)

class StructureResponse(StructureCreate):
    id: int

class DepartmentCreate(BaseModel):
    image: Optional[str] = None
    name: str
    head: str
    head_phone: Optional[str] = None
    head_email: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        image: UploadFile = File(None),
        name: str = Form(...),
        head: str = Form(...),
        head_phone: str = Form(None),
        head_email: str = Form(None)
    ):
        return cls(image=image, name=name, head=head, head_phone=head_phone, head_email=head_email)

class DepartmentResponse(DepartmentCreate):
    id: int

class VacancyCreate(BaseModel):
    title: str
    position: str
    department: str
    requirements: Optional[str] = None
    status: str

class VacancyResponse(VacancyCreate):
    id: int
    