from fastapi import FastAPI, Depends
from routers import auth, institute, documents, news, contact
import sqlite3
from dotenv import load_dotenv
import os
from fastapi_pagination import add_pagination
from passlib.context import CryptContext
from dependencies import get_language

# .env faylini yuklash
load_dotenv()

# FastAPI ilovasini yaratish
app = FastAPI()

# Routersni qo'shish
app.include_router(auth.router)
app.include_router(institute.router)
app.include_router(documents.router)
app.include_router(news.router)
app.include_router(contact.router)

# Pagination qo'shish
add_pagination(app)

# Parolni shifrlash uchun
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Ma'lumotlar bazasini yaratish
def init_db():
    conn = sqlite3.connect("tmsiti.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS institute_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            charter_pdf TEXT,
            statute_pdf TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS management (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            position TEXT NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            specialty TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS structure (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            name TEXT NOT NULL,
            head TEXT NOT NULL,
            head_phone TEXT,
            head_email TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            position TEXT NOT NULL,
            department TEXT NOT NULL,
            requirements TEXT,
            status TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS laws (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            order_number TEXT NOT NULL,
            adopted_date TEXT NOT NULL,
            effective_date TEXT NOT NULL,
            issuing_authority TEXT NOT NULL,
            link TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urban_norms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            norm_name TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS norm_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            norm_id INTEGER,
            group_name TEXT NOT NULL,
            FOREIGN KEY (norm_id) REFERENCES urban_norms(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS norm_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            norm_id INTEGER,
            group_id INTEGER,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            link TEXT NOT NULL,
            FOREIGN KEY (norm_id) REFERENCES urban_norms(id),
            FOREIGN KEY (group_id) REFERENCES norm_groups(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS standards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            pdf_link TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            pdf_link TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resource_norms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            pdf_link TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reference_docs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pdf_link TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL,
            link TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL,
            image TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS anticorruption (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL,
            document_link TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            sent_at TEXT NOT NULL
        )
    """)
    # Dastlabki admin foydalanuvchisini qo‘shish
    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        hashed_password = pwd_context.hash("admin")
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", hashed_password, "admin")
        )
    conn.commit()
    conn.close()

# Oddiy foydalanuvchi uchun endpoint
@app.get("/public/info")
async def public_info(lang: str = Depends(get_language)):
    return {"message": lang["messages"]["public_info"]}

# Dastur ishga tushganda DB ni tayyorlash
init_db()