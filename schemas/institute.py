from pydantic import BaseModel
from typing import Optional

class InstituteInfoCreate(BaseModel):
    content: str
    charter_pdf: Optional[str] = None
    statute_pdf: Optional[str] = None

class InstituteInfoResponse(InstituteInfoCreate):
    id: int

class ManagementCreate(BaseModel):
    image: Optional[str] = None
    position: str
    full_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    specialty: Optional[str] = None

class ManagementResponse(ManagementCreate):
    id: int

class StructureCreate(BaseModel):
    image: str

class StructureResponse(StructureCreate):
    id: int

class DepartmentCreate(BaseModel):
    image: Optional[str] = None
    name: str
    head: str
    head_phone: Optional[str] = None
    head_email: Optional[str] = None

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