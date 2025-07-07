from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from dependencies import get_db, get_language

load_dotenv()

router = APIRouter(prefix="/contact", tags=["contact"])

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

@router.post("/send")
async def send_contact_message(contact: ContactCreate, db: sqlite3.Connection = Depends(get_db), lang: dict = Depends(get_language)):
    # Ma'lumotlar bazasiga saqlash
    cursor = db.cursor()
    sent_at = datetime.utcnow().isoformat()
    cursor.execute(
        "INSERT INTO contacts (name, email, message, sent_at) VALUES (?, ?, ?, ?)",
        (contact.name, contact.email, contact.message, sent_at)
    )
    db.commit()

    # Email yuborish
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL")

    if not all([smtp_username, smtp_password, recipient_email]):
        raise HTTPException(status_code=500, detail="SMTP configuration is missing")

    msg = MIMEMultipart()
    msg["From"] = smtp_username
    msg["To"] = recipient_email
    msg["Subject"] = f"New Contact Message from {contact.name}"
    body = f"Name: {contact.name}\nEmail: {contact.email}\nMessage: {contact.message}\nSent at: {sent_at}"
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

    return {"message": lang["messages"]["message_sent"]}
