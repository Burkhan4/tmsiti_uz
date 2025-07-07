from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from typing import List
import sqlite3
from dependencies import get_db, get_current_admin
from schemas.documents import (
    LawCreate, LawResponse,
    UrbanNormCreate, UrbanNormResponse,
    NormGroupCreate, NormGroupResponse,
    NormDocumentCreate, NormDocumentResponse,
    StandardCreate, StandardResponse,
    RegulationCreate, RegulationResponse,
    ResourceNormCreate, ResourceNormResponse,
    ReferenceDocCreate, ReferenceDocResponse
)
from fastapi_pagination import Page, paginate
from utils.file_upload import save_file

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/laws", response_model=LawResponse)
async def create_law(
    name: str = Form(...),
    order_number: str = Form(...),
    adopted_date: str = Form(...),
    effective_date: str = Form(...),
    issuing_authority: str = Form(...),
    link: UploadFile = File(...),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    link_path = await save_file(link, ["pdf"], "uploads/laws")
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO laws (name, order_number, adopted_date, effective_date, issuing_authority, link) VALUES (?, ?, ?, ?, ?, ?)",
        (name, order_number, adopted_date, effective_date, issuing_authority, link_path)
    )
    db.commit()
    return {
        "id": cursor.lastrowid,
        "name": name,
        "order_number": order_number,
        "adopted_date": adopted_date,
        "effective_date": effective_date,
        "issuing_authority": issuing_authority,
        "link": link_path
    }

@router.get("/laws", response_model=List[LawResponse])
async def get_laws(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM laws")
    items = cursor.fetchall()
    return [
        {
            "id": item["id"],
            "name": item["name"],
            "order_number": item["order_number"],
            "adopted_date": item["adopted_date"],
            "effective_date": item["effective_date"],
            "issuing_authority": item["issuing_authority"],
            "link": item["link"]
        } for item in items
    ]

@router.put("/laws/{id}", response_model=LawResponse)
async def update_law(
    id: int,
    name: str = Form(...),
    order_number: str = Form(...),
    adopted_date: str = Form(...),
    effective_date: str = Form(...),
    issuing_authority: str = Form(...),
    link: UploadFile = File(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM laws WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Law not found")
    link_path = await save_file(link, ["pdf"], "uploads/laws") if link else None
    cursor.execute(
        "UPDATE laws SET name = ?, order_number = ?, adopted_date = ?, effective_date = ?, issuing_authority = ?, link = COALESCE(?, link) WHERE id = ?",
        (name, order_number, adopted_date, effective_date, issuing_authority, link_path, id)
    )
    db.commit()
    return {
        "id": id,
        "name": name,
        "order_number": order_number,
        "adopted_date": adopted_date,
        "effective_date": effective_date,
        "issuing_authority": issuing_authority,
        "link": link_path
    }

@router.delete("/laws/{id}")
async def delete_law(id: int, current_user: dict = Depends(get_current_admin), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM laws WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Law not found")
    cursor.execute("DELETE FROM laws WHERE id = ?", (id,))
    db.commit()
    return {"message": "Law deleted"}

@router.post("/urban-norms", response_model=UrbanNormResponse)
async def create_urban_norm(
    norm: UrbanNormCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("INSERT INTO urban_norms (norm_name) VALUES (?)", (norm.norm_name,))
    db.commit()
    return {"id": cursor.lastrowid, "norm_name": norm.norm_name}

@router.get("/urban-norms", response_model=List[UrbanNormResponse])
async def get_urban_norms(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM urban_norms")
    items = cursor.fetchall()
    return [{"id": item["id"], "norm_name": item["norm_name"]} for item in items]

@router.post("/urban-norms/{norm_id}/groups", response_model=NormGroupResponse)
async def create_norm_group(
    norm_id: int,
    group: NormGroupCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM urban_norms WHERE id = ?", (norm_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Urban norm not found")
    cursor.execute("INSERT INTO norm_groups (norm_id, group_name) VALUES (?, ?)", (norm_id, group.group_name))
    db.commit()
    return {"id": cursor.lastrowid, "norm_id": norm_id, "group_name": group.group_name}

@router.get("/urban-norms/{norm_id}/groups", response_model=List[NormGroupResponse])
async def get_norm_groups(norm_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM norm_groups WHERE norm_id = ?", (norm_id,))
    items = cursor.fetchall()
    return [{"id": item["id"], "norm_id": item["norm_id"], "group_name": item["group_name"]} for item in items]

@router.post("/urban-norms/{norm_id}/groups/{group_id}/documents", response_model=NormDocumentResponse)
async def create_norm_document(
    norm_id: int,
    group_id: int,
    code: str = Form(...),
    name: str = Form(...),
    link: UploadFile = File(...),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM urban_norms WHERE id = ?", (norm_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Urban norm not found")
    cursor.execute("SELECT * FROM norm_groups WHERE id = ? AND norm_id = ?", (group_id, norm_id))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Norm group not found")
    link_path = await save_file(link, ["pdf"], "uploads/norm_documents")
    cursor.execute(
        "INSERT INTO norm_documents (norm_id, group_id, code, name, link) VALUES (?, ?, ?, ?, ?)",
        (norm_id, group_id, code, name, link_path)
    )
    db.commit()
    return {"id": cursor.lastrowid, "norm_id": norm_id, "group_id": group_id, "code": code, "name": name, "link": link_path}

@router.get("/urban-norms/{norm_id}/groups/{group_id}/documents", response_model=List[NormDocumentResponse])
async def get_norm_documents(norm_id: int, group_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM norm_documents WHERE norm_id = ? AND group_id = ?", (norm_id, group_id))
    items = cursor.fetchall()
    return [
        {
            "id": item["id"],
            "norm_id": item["norm_id"],
            "group_id": item["group_id"],
            "code": item["code"],
            "name": item["name"],
            "link": item["link"]
        } for item in items
    ]

@router.post("/standards", response_model=StandardResponse)
async def create_standard(
    code: str = Form(...),
    name: str = Form(...),
    pdf_link: UploadFile = File(...),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    pdf_path = await save_file(pdf_link, ["pdf"], "uploads/standards")
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO standards (code, name, pdf_link) VALUES (?, ?, ?)",
        (code, name, pdf_path)
    )
    db.commit()
    return {"id": cursor.lastrowid, "code": code, "name": name, "pdf_link": pdf_path}

@router.get("/standards", response_model=List[StandardResponse])
async def get_standards(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM standards")
    items = cursor.fetchall()
    return [{"id": item["id"], "code": item["code"], "name": item["name"], "pdf_link": item["pdf_link"]} for item in items]

@router.put("/standards/{id}", response_model=StandardResponse)
async def update_standard(
    id: int,
    code: str = Form(...),
    name: str = Form(...),
    pdf_link: UploadFile = File(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM standards WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Standard not found")
    pdf_path = await save_file(pdf_link, ["pdf"], "uploads/standards") if pdf_link else None
    cursor.execute(
        "UPDATE standards SET code = ?, name = ?, pdf_link = COALESCE(?, pdf_link) WHERE id = ?",
        (code, name, pdf_path, id)
    )
    db.commit()
    return {"id": id, "code": code, "name": name, "pdf_link": pdf_path}

@router.delete("/standards/{id}")
async def delete_standard(id: int, current_user: dict = Depends(get_current_admin), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM standards WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Standard not found")
    cursor.execute("DELETE FROM standards WHERE id = ?", (id,))
    db.commit()
    return {"message": "Standard deleted"}

@router.post("/regulations", response_model=RegulationResponse)
async def create_regulation(
    code: str = Form(...),
    name: str = Form(...),
    pdf_link: UploadFile = File(...),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    pdf_path = await save_file(pdf_link, ["pdf"], "uploads/regulations")
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO regulations (code, name, pdf_link) VALUES (?, ?, ?)",
        (code, name, pdf_path)
    )
    db.commit()
    return {"id": cursor.lastrowid, "code": code, "name": name, "pdf_link": pdf_path}

@router.get("/regulations", response_model=List[RegulationResponse])
async def get_regulations(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM regulations")
    items = cursor.fetchall()
    return [{"id": item["id"], "code": item["code"], "name": item["name"], "pdf_link": item["pdf_link"]} for item in items]

@router.put("/regulations/{id}", response_model=RegulationResponse)
async def update_regulation(
    id: int,
    code: str = Form(...),
    name: str = Form(...),
    pdf_link: UploadFile = File(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM regulations WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Regulation not found")
    pdf_path = await save_file(pdf_link, ["pdf"], "uploads/regulations") if pdf_link else None
    cursor.execute(
        "UPDATE regulations SET code = ?, name = ?, pdf_link = COALESCE(?, pdf_link) WHERE id = ?",
        (code, name, pdf_path, id)
    )
    db.commit()
    return {"id": id, "code": code, "name": name, "pdf_link": pdf_path}

@router.delete("/regulations/{id}")
async def delete_regulation(id: int, current_user: dict = Depends(get_current_admin), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM regulations WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Regulation not found")
    cursor.execute("DELETE FROM regulations WHERE id = ?", (id,))
    db.commit()
    return {"message": "Regulation deleted"}

@router.post("/resource-norms", response_model=ResourceNormResponse)
async def create_resource_norm(
    code: str = Form(...),
    name: str = Form(...),
    pdf_link: UploadFile = File(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    pdf_path = await save_file(pdf_link, ["pdf"], "uploads/resource_norms") if pdf_link else None
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO resource_norms (code, name, pdf_link) VALUES (?, ?, ?)",
        (code, name, pdf_path)
    )
    db.commit()
    return {"id": cursor.lastrowid, "code": code, "name": name, "pdf_link": pdf_path}

@router.get("/resource-norms", response_model=List[ResourceNormResponse])
async def get_resource_norms(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM resource_norms")
    items = cursor.fetchall()
    return [{"id": item["id"], "code": item["code"], "name": item["name"], "pdf_link": item["pdf_link"]} for item in items]

@router.put("/resource-norms/{id}", response_model=ResourceNormResponse)
async def update_resource_norm(
    id: int,
    code: str = Form(...),
    name: str = Form(...),
    pdf_link: UploadFile = File(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM resource_norms WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Resource norm not found")
    pdf_path = await save_file(pdf_link, ["pdf"], "uploads/resource_norms") if pdf_link else None
    cursor.execute(
        "UPDATE resource_norms SET code = ?, name = ?, pdf_link = COALESCE(?, pdf_link) WHERE id = ?",
        (code, name, pdf_path, id)
    )
    db.commit()
    return {"id": id, "code": code, "name": name, "pdf_link": pdf_path}

@router.delete("/resource-norms/{id}")
async def delete_resource_norm(id: int, current_user: dict = Depends(get_current_admin), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM resource_norms WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Resource norm not found")
    cursor.execute("DELETE FROM resource_norms WHERE id = ?", (id,))
    db.commit()
    return {"message": "Resource norm deleted"}

@router.post("/reference-docs", response_model=ReferenceDocResponse)
async def create_reference_doc(
    name: str = Form(...),
    pdf_link: UploadFile = File(...),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    pdf_path = await save_file(pdf_link, ["pdf"], "uploads/reference_docs")
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO reference_docs (name, pdf_link) VALUES (?, ?)",
        (name, pdf_path)
    )
    db.commit()
    return {"id": cursor.lastrowid, "name": name, "pdf_link": pdf_path}

@router.get("/reference-docs", response_model=List[ReferenceDocResponse])
async def get_reference_docs(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reference_docs")
    items = cursor.fetchall()
    return [{"id": item["id"], "name": item["name"], "pdf_link": item["pdf_link"]} for item in items]

@router.put("/reference-docs/{id}", response_model=ReferenceDocResponse)
async def update_reference_doc(
    id: int,
    name: str = Form(...),
    pdf_link: UploadFile = File(None),
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reference_docs WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Reference doc not found")
    pdf_path = await save_file(pdf_link, ["pdf"], "uploads/reference_docs") if pdf_link else None
    cursor.execute(
        "UPDATE reference_docs SET name = ?, pdf_link = COALESCE(?, pdf_link) WHERE id = ?",
        (name, pdf_path, id)
    )
    db.commit()
    return {"id": id, "name": name, "pdf_link": pdf_path}

@router.delete("/reference-docs/{id}")
async def delete_reference_doc(id: int, current_user: dict = Depends(get_current_admin), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reference_docs WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Reference doc not found")
    cursor.execute("DELETE FROM reference_docs WHERE id = ?", (id,))
    db.commit()
    return {"message": "Reference doc deleted"}
