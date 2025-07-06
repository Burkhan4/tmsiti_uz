from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import sqlite3
from dependencies import get_db, get_current_admin
from schemas.institute import (
    InstituteInfoCreate, InstituteInfoResponse,
    ManagementCreate, ManagementResponse,
    StructureCreate, StructureResponse,
    DepartmentCreate, DepartmentResponse,
    VacancyCreate, VacancyResponse
)

router = APIRouter(prefix="/institute", tags=["institute"])

# INSTITUT HAQIDA
@router.post("/about", response_model=InstituteInfoResponse)
async def create_institute_info(
    info: InstituteInfoCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO institute_info (content, charter_pdf, statute_pdf) VALUES (?, ?, ?)",
        (info.content, info.charter_pdf, info.statute_pdf)
    )
    db.commit()
    return {**info.dict(), "id": cursor.lastrowid}

@router.get("/about", response_model=List[InstituteInfoResponse])
async def get_institute_info(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM institute_info")
    items = cursor.fetchall()
    return [{"id": item["id"], "content": item["content"], "charter_pdf": item["charter_pdf"], "statute_pdf": item["statute_pdf"]} for item in items]

@router.put("/about/{id}", response_model=InstituteInfoResponse)
async def update_institute_info(
    id: int,
    info: InstituteInfoCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM institute_info WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Institute info not found")
    cursor.execute(
        "UPDATE institute_info SET content = ?, charter_pdf = ?, statute_pdf = ? WHERE id = ?",
        (info.content, info.charter_pdf, info.statute_pdf, id)
    )
    db.commit()
    return {**info.dict(), "id": id}

@router.delete("/about/{id}")
async def delete_institute_info(
    id: int,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM institute_info WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Institute info not found")
    cursor.execute("DELETE FROM institute_info WHERE id = ?", (id,))
    db.commit()
    return {"message": "Institute info deleted"}

# RAHBARIYAT
@router.post("/management", response_model=ManagementResponse)
async def create_management(
    management: ManagementCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO management (image, position, full_name, phone, email, specialty) VALUES (?, ?, ?, ?, ?, ?)",
        (management.image, management.position, management.full_name, management.phone, management.email, management.specialty)
    )
    db.commit()
    return {**management.dict(), "id": cursor.lastrowid}

@router.get("/management", response_model=List[ManagementResponse])
async def get_management(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM management")
    items = cursor.fetchall()
    return [{"id": item["id"], "image": item["image"], "position": item["position"], "full_name": item["full_name"], "phone": item["phone"], "email": item["email"], "specialty": item["specialty"]} for item in items]

@router.put("/management/{id}", response_model=ManagementResponse)
async def update_management(
    id: int,
    management: ManagementCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM management WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Management not found")
    cursor.execute(
        "UPDATE management SET image = ?, position = ?, full_name = ?, phone = ?, email = ?, specialty = ? WHERE id = ?",
        (management.image, management.position, management.full_name, management.phone, management.email, management.specialty, id)
    )
    db.commit()
    return {**management.dict(), "id": id}

@router.delete("/management/{id}")
async def delete_management(
    id: int,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM management WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Management not found")
    cursor.execute("DELETE FROM management WHERE id = ?", (id,))
    db.commit()
    return {"message": "Management deleted"}

# TASHKILIY TUZILMA
@router.post("/structure", response_model=StructureResponse)
async def create_structure(
    structure: StructureCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("INSERT INTO structure (image) VALUES (?)", (structure.image,))
    db.commit()
    return {**structure.dict(), "id": cursor.lastrowid}

@router.get("/structure", response_model=List[StructureResponse])
async def get_structure(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM structure")
    items = cursor.fetchall()
    return [{"id": item["id"], "image": item["image"]} for item in items]

@router.put("/structure/{id}", response_model=StructureResponse)
async def update_structure(
    id: int,
    structure: StructureCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM structure WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Structure not found")
    cursor.execute("UPDATE structure SET image = ? WHERE id = ?", (structure.image, id))
    db.commit()
    return {**structure.dict(), "id": id}

@router.delete("/structure/{id}")
async def delete_structure(
    id: int,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM structure WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Structure not found")
    cursor.execute("DELETE FROM structure WHERE id = ?", (id,))
    db.commit()
    return {"message": "Structure deleted"}

# TARKIBIY BO'LINMALAR
@router.post("/departments", response_model=DepartmentResponse)
async def create_department(
    department: DepartmentCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO departments (image, name, head, head_phone, head_email) VALUES (?, ?, ?, ?, ?)",
        (department.image, department.name, department.head, department.head_phone, department.head_email)
    )
    db.commit()
    return {**department.dict(), "id": cursor.lastrowid}

@router.get("/departments", response_model=List[DepartmentResponse])
async def get_departments(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM departments")
    items = cursor.fetchall()
    return [{"id": item["id"], "image": item["image"], "name": item["name"], "head": item["head"], "head_phone": item["head_phone"], "head_email": item["head_email"]} for item in items]

@router.put("/departments/{id}", response_model=DepartmentResponse)
async def update_department(
    id: int,
    department: DepartmentCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM departments WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Department not found")
    cursor.execute(
        "UPDATE departments SET image = ?, name = ?, head = ?, head_phone = ?, head_email = ? WHERE id = ?",
        (department.image, department.name, department.head, department.head_phone, department.head_email, id)
    )
    db.commit()
    return {**department.dict(), "id": id}

@router.delete("/departments/{id}")
async def delete_department(
    id: int,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM departments WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Department not found")
    cursor.execute("DELETE FROM departments WHERE id = ?", (id,))
    db.commit()
    return {"message": "Department deleted"}

# VAKANSIYALAR
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
async def delete_vacancy(
    id: int,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM vacancies WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Vacancy not found")
    cursor.execute("DELETE FROM vacancies WHERE id = ?", (id,))
    db.commit()
    return {"message": "Vacancy deleted"}