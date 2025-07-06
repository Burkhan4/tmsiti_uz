from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import sqlite3
from typing import Optional
from dotenv import load_dotenv
import os

# .env faylini yuklash
load_dotenv()

# JWT sozlamalari
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"


# JWT sozlamalari
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Tokenni HTTPBearer orqali olish
oauth2_scheme = HTTPBearer()

# SQLite ma'lumotlar bazasi bilan ulanish
def get_db():
    conn = sqlite3.connect("tmsiti.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Foydalanuvchini token orqali olish
async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: sqlite3.Connection = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user is None:
        raise credentials_exception
    return user

# Faqat admin uchun endpointlarni himoyalash
async def get_current_admin(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user