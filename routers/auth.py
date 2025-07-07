from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
import sqlite3
from passlib.context import CryptContext
from dependencies import get_db, get_current_admin, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["auth"])

# Parolni shifrlash uchun
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Foydalanuvchi modeli
class User(BaseModel):
    username: str
    password: str
    role: str = "admin"

class Token(BaseModel):
    access_token: str
    token_type: str

# Parolni shifrlash va tekshirish
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# JWT token yaratish
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Foydalanuvchini autentifikatsiya qilish
def authenticate_user(username: str, password: str, db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user or not verify_password(password, user["password"]):
        return False
    return user

# Token olish uchun endpoint
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: sqlite3.Connection = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Admin endpointi: yangi foydalanuvchi yaratish
@router.post("/register")
async def register_user(
    user: User,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (user.username, hashed_password, user.role)
    )
    db.commit()
    return {"message": f"User {user.username} created successfully"}

# Admin endpointi: foydalanuvchilar ro‘yxati
@router.get("/users")
async def get_users(
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT username, role FROM users")
    users = cursor.fetchall()
    return [{"username": user["username"], "role": user["role"]} for user in users]
