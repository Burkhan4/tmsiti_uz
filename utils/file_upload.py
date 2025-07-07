import os
from fastapi import UploadFile, HTTPException
import shutil
from datetime import datetime

async def save_file(file: UploadFile, allowed_extensions: list[str], upload_dir: str = "uploads"):
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    extension = file.filename.split(".")[-1].lower()
    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"File extension {extension} not allowed. Allowed: {allowed_extensions}")
    
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return f"/{file_path}"
