from pydantic import BaseModel
from typing import Optional
from fastapi import Form, File, UploadFile

class AnnouncementCreate(BaseModel):
    title: str
    content: str
    date: str
    link: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        content: str = Form(...),
        date: str = Form(...),
        link: str = Form(None)
    ):
        return cls(title=title, content=content, date=date, link=link)

class AnnouncementResponse(AnnouncementCreate):
    id: int

class NewsCreate(BaseModel):
    title: str
    content: str
    date: str
    image: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        content: str = Form(...),
        date: str = Form(...),
        image: UploadFile = File(None)
    ):
        return cls(title=title, content=content, date=date, image=image)

class NewsResponse(NewsCreate):
    id: int

class AnticorruptionCreate(BaseModel):
    title: str
    content: str
    date: str
    document_link: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        content: str = Form(...),
        date: str = Form(...),
        document_link: UploadFile = File(None)
    ):
        return cls(title=title, content=content, date=date, document_link=document_link)

class AnticorruptionResponse(AnticorruptionCreate):
    id: int
    