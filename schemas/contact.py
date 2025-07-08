from pydantic import BaseModel
from typing import Optional
from fastapi import Form, File, UploadFile

class ContactCreate(BaseModel):
    name: str
    email: str
    subject: str
    message: str
    file: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        email: str = Form(...),
        subject: str = Form(...),
        message: str = Form(...),
        file: UploadFile = File(None)
    ):
        return cls(name=name, email=email, subject=subject, message=message, file=file)

class ContactResponse(ContactCreate):
    id: int