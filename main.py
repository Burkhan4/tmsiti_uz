from fastapi import FastAPI
from routers import auth, institute, documents, news, contact
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(institute.router)
app.include_router(documents.router)
app.include_router(news.router)
app.include_router(contact.router)

def init_db():
    with sqlite3.connect("tmsiti.db") as db:
        cursor = db.cursor()
        # Contacts jadvali
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                file TEXT
            )
        """)
        # Users jadvali
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)
        # Institute info jadvali
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS institute_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                charter_pdf TEXT,
                statute_pdf TEXT
            )
        """)
        # Management jadvali
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
        # Structure jadvali
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS structure (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image TEXT NOT NULL
            )
        """)
        # Departments jadvali
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
        # Vacancies jadvali
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                department TEXT NOT NULL,
                requirements TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)
        # Announcements jadvali
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS announcements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                date TEXT NOT NULL,
                image TEXT,
                link TEXT
            )
        """)
        # News jadvali
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                date TEXT NOT NULL,
                image TEXT
            )
        """)
        # Anticorruption jadvali
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anticorruption (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                minister_message TEXT,
                date TEXT NOT NULL,
                image TEXT,
                document_link TEXT,
                telegram_link TEXT
            )
        """)
        # Default admin
        cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                      ("admin", "$2b$12$cuzkTEoOTLv9RI45wvJWOu4zmyZl78Jpv8R0yI/os8NdV557U9rLi", "admin"))
        db.commit()

def update_db_schema():
    with sqlite3.connect("tmsiti.db") as db:
        cursor = db.cursor()
        # Subject ustunini qo'shish
        try:
            cursor.execute("ALTER TABLE contacts ADD COLUMN subject TEXT NOT NULL DEFAULT ''")
        except sqlite3.OperationalError:
            pass  # Ustun allaqachon mavjud bo'lsa
        # File ustunini qo'shish
        try:
            cursor.execute("ALTER TABLE contacts ADD COLUMN file TEXT")
        except sqlite3.OperationalError:
            pass  # Ustun allaqachon mavjud bo'lsa
        db.commit()

@app.on_event("startup")
async def startup_event():
    init_db()
    update_db_schema()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)