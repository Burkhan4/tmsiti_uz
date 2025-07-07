from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from typing import List
from schemas.institute import (
    InstituteInfoCreate, InstituteInfoResponse,
    ManagementCreate, ManagementResponse,
    StructureCreate, StructureResponse,
    DepartmentCreate, DepartmentResponse,
    VacancyCreate, VacancyResponse
)
from dependencies import get_db, get_current_admin
from fastapi_pagination import Page, paginate
from utils.file_upload import save_file
import sqlite3

router = APIRouter(prefix="/institute", tags=["institute"])

@router.post("/about", response_model=InstituteInfoResponse)
async def create_institute_info(
    content: str = Form(...),
    charter_pdf: UploadFile = File(None),
    statute_pdf: UploadFile = File(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    charter_path = await save_file(charter_pdf, ["pdf"], "uploads/institute") if charter_pdf else None
    statute_path = await save_file(statute_pdf, ["pdf"], "uploads/institute") if statute_pdf else None
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO institute_info (content, charter_pdf, statute_pdf) VALUES (?, ?, ?)",
        (content, charter_path, statute_path)
    )
    db.commit()
    return {"id": cursor.lastrowid, "content": content, "charter_pdf": charter_path, "statute_pdf": statute_path}

@router.get("/about", response_model=List[InstituteInfoResponse])
async def get_institute_info(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM institute_info")
    items = cursor.fetchall()
    return [{"id": item["id"], "content": item["content"], "charter_pdf": item["charter_pdf"], "statute_pdf": item["statute_pdf"]} for item in items]

@router.put("/about/{id}", response_model=InstituteInfoResponse)
async def update_institute_info(
    id: int,
    content: str = Form(...),
    charter_pdf: UploadFile = File(None),
    statute_pdf: UploadFile = File(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM institute_info WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Institute info not found")
    charter_path = await save_file(charter_pdf, ["pdf"], "uploads/institute") if charter_pdf else None
    statute_path = await save_file(statute_pdf, ["pdf"], "uploads/institute") if statute_pdf else None
    cursor.execute(
        "UPDATE institute_info SET content = ?, charter_pdf = COALESCE(?, charter_pdf), statute_pdf = COALESCE(?, statute_pdf) WHERE id = ?",
        (content, charter_path, statute_path, id)
    )
    db.commit()
    return {"id": id, "content": content, "charter_pdf": charter_path, "statute_pdf": statute_path}

@router.delete("/about/{id}")
async def delete_institute_info(id: int, current_user: dict = Depends(get_current_admin), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM institute_info WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Institute info not found")
    cursor.execute("DELETE FROM institute_info WHERE id = ?", (id,))
    db.commit()
    return {"message": "Institute info deleted"}

@router.post("/management", response_model=ManagementResponse)
async def create_management(
    image: UploadFile = File(None),
    position: str = Form(...),
    full_name: str = Form(...),
    phone: str = Form(None),
    email: str = Form(None),
    specialty: str = Form(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    image_path = await save_file(image, ["jpg", "png"], "uploads/management") if image else None
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO management (image, position, full_name, phone, email, specialty) VALUES (?, ?, ?, ?, ?, ?)",
        (image_path, position, full_name, phone, email, specialty)
    )
    db.commit()
    return {"id": cursor.lastrowid, "image": image_path, "position": position, "full_name": full_name, "phone": phone, "email": email, "specialty": specialty}

@router.get("/management", response_model=List[ManagementResponse])
async def get_management(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM management")
    items = cursor.fetchall()
    return [{"id": item["id"], "image": item["image"], "position": item["position"], "full_name": item["full_name"], "phone": item["phone"], "email": item["email"], "specialty": item["specialty"]} for item in items]

@router.put("/management/{id}", response_model=ManagementResponse)
async def update_management(
    id: int,
    image: UploadFile = File(None),
    position: str = Form(...),
    full_name: str = Form(...),
    phone: str = Form(None),
    email: str = Form(None),
    specialty: str = Form(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM management WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Management not found")
    image_path = await save_file(image, ["jpg", "png"], "uploads/management") if image else None
    cursor.execute(
        "UPDATE management SET image = COALESCE(?, image), position = ?, full_name = ?, phone = ?, email = ?, specialty = ? WHERE id = ?",
        (image_path, position, full_name, phone, email, specialty, id)
    )
    db.commit()
    return {"id": id, "image": image_path, "position": position, "full_name": full_name, "phone": phone, "email": email, "specialty": specialty}

@router.delete("/management/{id}")
async def delete_management(id: int, current_user: dict = Depends(get_current_admin), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM management WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Management not found")
    cursor.execute("DELETE FROM management WHERE id = ?", (id,))
    db.commit()
    return {"message": "Management deleted"}

@router.post("/structure", response_model=StructureResponse)
async def create_structure(
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    image_path = await save_file(image, ["jpg", "png"], "uploads/structure")
    cursor = db.cursor()
    cursor.execute("INSERT INTO structure (image) VALUES (?)", (image_path,))
    db.commit()
    return {"id": cursor.lastrowid, "image": image_path}

@router.get("/structure", response_model=List[StructureResponse])
async def get_structure(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM structure")
    items = cursor.fetchall()
    return [{"id": item["id"], "image": item["image"]} for item in items]

@router.put("/structure/{id}", response_model=StructureResponse)
async def update_structure(
    id: int,
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM structure WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Structure not found")
    image_path = await save_file(image, ["jpg", "png"], "uploads/structure")
    cursor.execute("UPDATE structure SET image = ? WHERE id = ?", (image_path, id))
    db.commit()
    return {"id": id, "image": image_path}

@router.delete("/structure/{id}")
async def delete_structure(id: int, current_user: dict = Depends(get_current_admin), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM structure WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Structure not found")
    cursor.execute("DELETE FROM structure WHERE id = ?", (id,))
    db.commit()
    return {"message": "Structure deleted"}

@router.post("/departments", response_model=DepartmentResponse)
async def create_department(
    image: UploadFile = File(None),
    name: str = Form(...),
    head: str = Form(...),
    head_phone: str = Form(None),
    head_email: str = Form(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    image_path = await save_file(image, ["jpg", "png"], "uploads/departments") if image else None
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO departments (image, name, head, head_phone, head_email) VALUES (?, ?, ?, ?, ?)",
        (image_path, name, head, head_phone, head_email)
    )
    db.commit()
    return {"id": cursor.lastrowid, "image": image_path, "name": name, "head": head, "head_phone": head_phone, "head_email": head_email}

@router.get("/departments", response_model=List[DepartmentResponse])
async def get_departments(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM departments")
    items = cursor.fetchall()
    return [{"id": item["id"], "image": item["image"], "name": item["name"], "head": item["head"], "head_phone": item["head_phone"], "head_email": item["head_email"]} for item in items]

@router.put("/departments/{id}", response_model=DepartmentResponse)
async def update_department(
    id: int,
    image: UploadFile = File(None),
    name: str = Form(...),
    head: str = Form(...),
    head_phone: str = Form(None),
    head_email: str = Form(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM departments WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Department not found")
    image_path = await save_file(image, ["jpg", "png"], "uploads/departments") if image else None
    cursor.execute(
        "UPDATE departments SET image = COALESCE(?, image), name = ?, head = ?, head_phone = ?, head_email = ? WHERE id = ?",
        (image_path, name, head, head_phone, head_email, id)
    )
    db.commit()
    return {"id": id, "image": image_path, "name": name, "head": head, "head_phone": head_phone, "head_email": head_email}

@router.delete("/departments/{id}")
async def delete_department(id: int, current_user: dict = Depends(get_current_admin), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM departments WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Department not found")
    cursor.execute("DELETE FROM departments WHERE id = ?", (id,))
    db.commit()
    return {"message": "Department deleted"}

@router.post("/vacancies", response_model=VacancyResponse)
async def create_vacancy(
    vacancy: VacancyCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO vacancies (title, position, department, requirements, status) VALUES (?, ?, ?, ?, ?)",
        (vacancy.title, vacancy.position, vacancy.department, vacancy.requirements, vacancy.status)
    )
    db.commit()
    return {**vacancy.dict(), "id": cursor.lastrowid}

@router.get("/vacancies", response_model=List[VacancyResponse])
async def get_vacancies(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM vacancies")
    items = cursor.fetchall()
    return [{"id": item["id"], "title": item["title"], "position": item["position"], "department": item["department"], "requirements": item["requirements"], "status": item["status"]} for item in items]

@router.put("/vacancies/{id}", response_model=VacancyResponse)
async def update_vacancy(
    id: int,
    vacancy: VacancyCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM vacancies WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Vacancy not found")
    cursor.execute(
        "UPDATE vacancies SET title = ?, position = ?, department = ?, requirements = ?, status = ? WHERE id = ?",
        (vacancy.title, vacancy.position, vacancy.department, vacancy.requirements, vacancy.status, id)
    )
    db.commit()
    return {**vacancy.dict(), "id": id}

@router.delete("/vacancies/{id}")
async def delete_vacancy(id: int, current_user: dict = Depends(get_current_admin), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM vacancies WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Vacancy not found")
    cursor.execute("DELETE FROM vacancies WHERE id = ?", (id,))
    db.commit()
    return {"message": "Vacancy deleted"}
