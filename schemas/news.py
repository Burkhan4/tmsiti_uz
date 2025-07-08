from pydantic import BaseModel
from typing import Optional
from fastapi import Form, File, UploadFile

class AnnouncementCreate(BaseModel):
    title: str
    content: str
    date: str
    image: Optional[str] = None
    link: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        content: str = Form(...),
        date: str = Form(...),
        image: UploadFile = File(None),
        link: str = Form(None)
    ):
        return cls(title=title, content=content, date=date, image=image, link=link)

class AnnouncementResponse(AnnouncementCreate):
    id: int

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
    minister_message: Optional[str] = None
    date: str
    image: Optional[str] = None
    document_link: Optional[str] = None
    telegram_link: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        content: str = Form(...),
        minister_message: str = Form(None),
        date: str = Form(...),
        image: UploadFile = File(None),
        document_link: UploadFile = File(None),
        telegram_link: str = Form(None)
    ):
        return cls(
            title=title,
            content=content,
            minister_message=minister_message,
            date=date,
            image=image,
            document_link=document_link,
            telegram_link=telegram_link
        )

class AnticorruptionResponse(AnticorruptionCreate):
    id: int
