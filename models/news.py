from pydantic import BaseModel, HttpUrl
from datetime import date
from typing import Optional

class Announcement(BaseModel):
    title: str
    content: str
    date: date
    link: Optional[HttpUrl] = None

class News(BaseModel):
    title: str
    content: str
    date: date
    image: Optional[HttpUrl] = None

class Anticorruption(BaseModel):
    title: str
    content: str
    date: date
    document_link: Optional[HttpUrl] = None