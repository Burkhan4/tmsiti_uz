from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from schemas.contact import ContactCreate, ContactResponse
import sqlite3
from dependencies import get_db
from aiogram import Bot
from aiogram.enums import ParseMode
import os
from dotenv import load_dotenv
from utils.file_upload import save_file

load_dotenv()

router = APIRouter(prefix="/contact", tags=["contact"])

@router.post("/send", response_model=ContactResponse)
async def send_contact_message(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    file: UploadFile = File(None),
    db: sqlite3.Connection = Depends(get_db)
):
    file_path = await save_file(file, ["pdf"], "uploads/contact") if file else None
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO contacts (name, email, subject, message, file) VALUES (?, ?, ?, ?, ?)",
        (name, email, subject, message, file_path)
    )
    db.commit()
    
    bot_token = os.getenv("BOT_TOKEN")
    telegram_user_id = os.getenv("TELEGRAM_USER_ID")
    
    if not bot_token or not telegram_user_id:
        raise HTTPException(status_code=500, detail="Telegram bot sozlamalari topilmadi")
    
    bot = Bot(token=bot_token)
    try:
        message_text = (
            f"Yangi xabar keldi!\n"
            f"Ism: {name}\n"
            f"Email: {email}\n"
            f"Mavzu: {subject}\n"
            f"Xabar: {message}\n"
            f"Fayl: {file_path if file_path else 'Yo‘q'}"
        )
        # Markdown o'rniga oddiy matn sifatida yuborish
        await bot.send_message(
            chat_id=telegram_user_id,
            text=message_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Telegram bot xatosi: {str(e)}")
    finally:
        await bot.session.close()
    
    return {"id": cursor.lastrowid, "name": name, "email": email, "subject": subject, "message": message, "file": file_path}

@router.get("/messages", response_model=list[ContactResponse])
async def get_contact_messages(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contacts")
    items = cursor.fetchall()
    return [{"id": item["id"], "name": item["name"], "email": item["email"], "subject": item["subject"], "message": item["message"], "file": item["file"]} for item in items]