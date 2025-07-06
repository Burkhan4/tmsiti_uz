from pydantic import BaseModel
from typing import Optional

class InstituteInfo(BaseModel):
    content: str
    charter_pdf: Optional[str] = None
    statute_pdf: Optional[str] = None

class Management(BaseModel):
    image: Optional[str] = None
    position: str
    full_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    specialty: Optional[str] = None

class Structure(BaseModel):
    image: str

class Department(BaseModel):
    image: Optional[str] = None
    name: str
    head: str
    head_phone: Optional[str] = None
    head_email: Optional[str] = None

class Vacancy(BaseModel):
    title: str
    position: str
    department: str
    requirements: Optional[str] = None
    status: str