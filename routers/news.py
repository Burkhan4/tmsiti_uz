from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from typing import List
import sqlite3
from dependencies import get_db, get_current_admin
from schemas.news import (
    AnnouncementCreate, AnnouncementResponse,
    NewsCreate, NewsResponse,
    AnticorruptionCreate, AnticorruptionResponse
)
from fastapi_pagination import Page, paginate
from utils.file_upload import save_file

router = APIRouter(prefix="/news", tags=["news"])

# E'LONLAR
@router.post("/announcements", response_model=AnnouncementResponse)
async def create_announcement(
    title: str = Form(...),
    content: str = Form(...),
    date: str = Form(...),
    image: UploadFile = File(None),
    link: str = Form(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    image_path = await save_file(image, ["jpg", "png"], "uploads/announcements") if image else None
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO announcements (title, content, date, image, link) VALUES (?, ?, ?, ?, ?)",
        (title, content, date, image_path, link)
    )
    db.commit()
    return {"id": cursor.lastrowid, "title": title, "content": content, "date": date, "image": image_path, "link": link}

@router.get("/announcements", response_model=List[AnnouncementResponse])
async def get_announcements(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM announcements")
    items = cursor.fetchall()
    return [{"id": item["id"], "title": item["title"], "content": item["content"], "date": item["date"], "link": item["link"]} for item in items]

@router.put("/announcements/{id}", response_model=AnnouncementResponse)
async def update_announcement(
    id: int,
    title: str = Form(...),
    content: str = Form(...),
    date: str = Form(...),
    link: str = Form(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM announcements WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Announcement not found")
    cursor.execute(
        "UPDATE announcements SET title = ?, content = ?, date = ?, link = ? WHERE id = ?",
        (title, content, date, link, id)
    )
    db.commit()
    return {"id": id, "title": title, "content": content, "date": date, "link": link}

@router.delete("/announcements/{id}")
async def delete_announcement(
    id: int,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM announcements WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Announcement not found")
    cursor.execute("DELETE FROM announcements WHERE id = ?", (id,))
    db.commit()
    return {"message": "Announcement deleted"}

# YANGILIK
@router.post("/news", response_model=NewsResponse)
async def create_news(
    title: str = Form(...),
    content: str = Form(...),
    date: str = Form(...),
    image: UploadFile = File(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    image_path = await save_file(image, ["jpg", "png"], "uploads/news") if image else None
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO news (title, content, date, image) VALUES (?, ?, ?, ?)",
        (title, content, date, image_path)
    )
    db.commit()
    return {"id": cursor.lastrowid, "title": title, "content": content, "date": date, "image": image_path}

@router.get("/news", response_model=Page[NewsResponse])
async def get_news(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM news")
    items = cursor.fetchall()
    return paginate([{"id": item["id"], "title": item["title"], "content": item["content"], "date": item["date"], "image": item["image"]} for item in items])

@router.put("/news/{id}", response_model=NewsResponse)
async def update_news(
    id: int,
    title: str = Form(...),
    content: str = Form(...),
    date: str = Form(...),
    image: UploadFile = File(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM news WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="News not found")
    image_path = await save_file(image, ["jpg", "png"], "uploads/news") if image else None
    cursor.execute(
        "UPDATE news SET title = ?, content = ?, date = ?, image = COALESCE(?, image) WHERE id = ?",
        (title, content, date, image_path, id)
    )
    db.commit()
    return {"id": id, "title": title, "content": content, "date": date, "image": image_path}

@router.delete("/news/{id}")
async def delete_news(
    id: int,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM news WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="News not found")
    cursor.execute("DELETE FROM news WHERE id = ?", (id,))
    db.commit()
    return {"message": "News deleted"}

@router.get("/news/{id}", response_model=NewsResponse)
async def get_news_detail(id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM news WHERE id = ?", (id,))
    item = cursor.fetchone()
    if not item:
        raise HTTPException(status_code=404, detail="News not found")
    return {"id": item["id"], "title": item["title"], "content": item["content"], "date": item["date"], "image": item["image"]}

@router.get("/related-news", response_model=List[NewsResponse])
async def get_related_news(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM news ORDER BY date DESC LIMIT 5")
    items = cursor.fetchall()
    return [{"id": item["id"], "title": item["title"], "content": item["content"], "date": item["date"], "image": item["image"]} for item in items]

# KORRUPSIYAGA QARSHI KURASHISH
@router.post("/anticorruption", response_model=AnticorruptionResponse)
async def create_anticorruption(
    title: str = Form(...),
    content: str = Form(...),
    minister_message: str = Form(None),
    date: str = Form(...),
    image: UploadFile = File(None),
    document_link: UploadFile = File(None),
    telegram_link: str = Form(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    image_path = await save_file(image, ["jpg", "png"], "uploads/anticorruption") if image else None
    doc_path = await save_file(document_link, ["pdf"], "uploads/anticorruption") if document_link else None
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO anticorruption (title, content, minister_message, date, image, document_link, telegram_link) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (title, content, minister_message, date, image_path, doc_path, telegram_link)
    )
    db.commit()
    return {
        "id": cursor.lastrowid,
        "title": title,
        "content": content,
        "minister_message": minister_message,
        "date": date,
        "image": image_path,
        "document_link": doc_path,
        "telegram_link": telegram_link
    }

@router.get("/anticorruption", response_model=List[AnticorruptionResponse])
async def get_anticorruption(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM anticorruption")
    items = cursor.fetchall()
    return [{"id": item["id"], "title": item["title"], "content": item["content"], "date": item["date"], "document_link": item["document_link"]} for item in items]

@router.put("/anticorruption/{id}", response_model=AnticorruptionResponse)
async def update_anticorruption(
    id: int,
    title: str = Form(...),
    content: str = Form(...),
    date: str = Form(...),
    document_link: UploadFile = File(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM anticorruption WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Anticorruption not found")
    doc_path = await save_file(document_link, ["pdf"], "uploads/anticorruption") if document_link else None
    cursor.execute(
        "UPDATE anticorruption SET title = ?, content = ?, date = ?, document_link = COALESCE(?, document_link) WHERE id = ?",
        (title, content, date, doc_path, id)
    )
    db.commit()
    return {"id": id, "title": title, "content": content, "date": date, "document_link": doc_path}

@router.delete("/anticorruption/{id}")
async def delete_anticorruption(
    id: int,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM anticorruption WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Anticorruption not found")
    cursor.execute("DELETE FROM anticorruption WHERE id = ?", (id,))
    db.commit()
    return {"message": "Anticorruption deleted"}
