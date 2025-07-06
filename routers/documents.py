from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import sqlite3
from dependencies import get_db, get_current_admin
from schemas.documents import (
    LawCreate, LawResponse,
    NormCreate, NormResponse,
    NormGroupCreate, NormGroupResponse,
    NormDocumentCreate, NormDocumentResponse,
    StandardCreate, StandardResponse,
    RegulationCreate, RegulationResponse,
    ResourceNormCreate, ResourceNormResponse,
    ReferenceCreate, ReferenceResponse
)
from fastapi_pagination import Page, paginate

router = APIRouter(prefix="/documents", tags=["documents"])

# QONUN, QAROR VA FARMONLAR
@router.post("/laws", response_model=LawResponse)
async def create_law(
    law: LawCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO laws (name, order_number, adopted_date, effective_date, issuing_authority, link) VALUES (?, ?, ?, ?, ?, ?)",
        (law.name, law.order_number, law.adopted_date, law.effective_date, law.issuing_authority, law.link)
    )
    db.commit()
    return {**law.dict(), "id": cursor.lastrowid}

@router.get("/laws", response_model=List[LawResponse])
async def get_laws(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM laws")
    items = cursor.fetchall()
    return [{"id": item["id"], "name": item["name"], "order_number": item["order_number"], "adopted_date": item["adopted_date"], "effective_date": item["effective_date"], "issuing_authority": item["issuing_authority"], "link": item["link"]} for item in items]

@router.put("/laws/{id}", response_model=LawResponse)
async def update_law(
    id: int,
    law: LawCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM laws WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Law not found")
    cursor.execute(
        "UPDATE laws SET name = ?, order_number = ?, adopted_date = ?, effective_date = ?, issuing_authority = ?, link = ? WHERE id = ?",
        (law.name, law.order_number, law.adopted_date, law.effective_date, law.issuing_authority, law.link, id)
    )
    db.commit()
    return {**law.dict(), "id": id}

@router.delete("/laws/{id}")
async def delete_law(
    id: int,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM laws WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Law not found")
    cursor.execute("DELETE FROM laws WHERE id = ?", (id,))
    db.commit()
    return {"message": "Law deleted"}

# SHAHARSOZLIK NORMALARI VA QOIDALARI
@router.post("/urban-norms", response_model=NormResponse)
async def create_norm(
    norm: NormCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("INSERT INTO urban_norms (norm_name) VALUES (?)", (norm.norm_name,))
    db.commit()
    return {**norm.dict(), "id": cursor.lastrowid}

@router.get("/urban-norms", response_model=List[NormResponse])
async def get_norms(db: sqlite3.Connection = Depends(get_db)):
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
        raise HTTPException(status_code=404, detail="Norm not found")
    cursor.execute("INSERT INTO norm_groups (norm_id, group_name) VALUES (?, ?)", (norm_id, group.group_name))
    db.commit()
    return {**group.dict(), "id": cursor.lastrowid}

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
    document: NormDocumentCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM urban_norms WHERE id = ?", (norm_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Norm not found")
    cursor.execute("SELECT * FROM norm_groups WHERE id = ? AND norm_id = ?", (group_id, norm_id))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Group not found")
    cursor.execute(
        "INSERT INTO norm_documents (norm_id, group_id, code, name, link) VALUES (?, ?, ?, ?, ?)",
        (norm_id, group_id, document.code, document.name, document.link)
    )
    db.commit()
    return {**document.dict(), "id": cursor.lastrowid}

@router.get("/urban-norms/{norm_id}/groups/{group_id}/documents", response_model=List[NormDocumentResponse])
async def get_norm_documents(norm_id: int, group_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM norm_documents WHERE norm_id = ? AND group_id = ?", (norm_id, group_id))
    items = cursor.fetchall()
    return [{"id": item["id"], "norm_id": item["norm_id"], "group_id": item["group_id"], "code": item["code"], "name": item["name"], "link": item["link"]} for item in items]

@router.put("/urban-norms/{norm_id}/groups/{group_id}/documents/{id}", response_model=NormDocumentResponse)
async def update_norm_document(
    norm_id: int,
    group_id: int,
    id: int,
    document: NormDocumentCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM norm_documents WHERE id = ? AND norm_id = ? AND group_id = ?", (id, norm_id, group_id))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Document not found")
    cursor.execute(
        "UPDATE norm_documents SET code = ?, name = ?, link = ? WHERE id = ?",
        (document.code, document.name, document.link, id)
    )
    db.commit()
    return {**document.dict(), "id": id}

@router.delete("/urban-norms/{norm_id}/groups/{group_id}/documents/{id}")
async def delete_norm_document(
    norm_id: int,
    group_id: int,
    id: int,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM norm_documents WHERE id = ? AND norm_id = ? AND group_id = ?", (id, norm_id, group_id))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Document not found")
    cursor.execute("DELETE FROM norm_documents WHERE id = ?", (id,))
    db.commit()
    return {"message": "Document deleted"}

# STANDARTLAR
@router.post("/standards", response_model=StandardResponse)
async def create_standard(
    standard: StandardCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO standards (code, name, pdf_link) VALUES (?, ?, ?)",
        (standard.code, standard.name, standard.pdf_link)
    )
    db.commit()
    return {**standard.dict(), "id": cursor.lastrowid}

@router.get("/standards", response_model=Page[StandardResponse])
async def get_standards(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM standards")
    items = cursor.fetchall()
    return paginate([{"id": item["id"], "code": item["code"], "name": item["name"], "pdf_link": item["pdf_link"]} for item in items])

@router.put("/standards/{id}", response_model=StandardResponse)
async def update_standard(
    id: int,
    standard: StandardCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM standards WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Standard not found")
    cursor.execute(
        "UPDATE standards SET code = ?, name = ?, pdf_link = ? WHERE id = ?",
        (standard.code, standard.name, standard.pdf_link, id)
    )
    db.commit()
    return {**standard.dict(), "id": id}

@router.delete("/standards/{id}")
async def delete_standard(
    id: int,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM standards WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Standard not found")
    cursor.execute("DELETE FROM standards WHERE id = ?", (id,))
    db.commit()
    return {"message": "Standard deleted"}

# QURILISH REGLAMENTLARI
@router.post("/regulations", response_model=RegulationResponse)
async def create_regulation(
    regulation: RegulationCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO regulations (code, name, pdf_link) VALUES (?, ?, ?)",
        (regulation.code, regulation.name, regulation.pdf_link)
    )
    db.commit()
    return {**regulation.dict(), "id": cursor.lastrowid}

@router.get("/regulations", response_model=List[RegulationResponse])
async def get_regulations(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM regulations")
    items = cursor.fetchall()
    return [{"id": item["id"], "code": item["code"], "name": item["name"], "pdf_link": item["pdf_link"]} for item in items]

@router.put("/regulations/{id}", response_model=RegulationResponse)
async def update_regulation(
    id: int,
    regulation: RegulationCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM regulations WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Regulation not found")
    cursor.execute(
        "UPDATE regulations SET code = ?, name = ?, pdf_link = ? WHERE id = ?",
        (regulation.code, regulation.name, regulation.pdf_link, id)
    )
    db.commit()
    return {**regulation.dict(), "id": id}

@router.delete("/regulations/{id}")
async def delete_regulation(
    id: int,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM regulations WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Regulation not found")
    cursor.execute("DELETE FROM regulations WHERE id = ?", (id,))
    db.commit()
    return {"message": "Regulation deleted"}

# SMETA-RESURS NORMALARI
@router.post("/resource-norms", response_model=ResourceNormResponse)
async def create_resource_norm(
    resource_norm: ResourceNormCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO resource_norms (code, name, pdf_link) VALUES (?, ?, ?)",
        (resource_norm.code, resource_norm.name, resource_norm.pdf_link)
    )
    db.commit()
    return {**resource_norm.dict(), "id": cursor.lastrowid}

@router.get("/resource-norms", response_model=List[ResourceNormResponse])
async def get_resource_norms(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM resource_norms")
    items = cursor.fetchall()
    return [{"id": item["id"], "code": item["code"], "name": item["name"], "pdf_link": item["pdf_link"]} for item in items]

@router.put("/resource-norms/{id}", response_model=ResourceNormResponse)
async def update_resource_norm(
    id: int,
    resource_norm: ResourceNormCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM resource_norms WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Resource norm not found")
    cursor.execute(
        "UPDATE resource_norms SET code = ?, name = ?, pdf_link = ? WHERE id = ?",
        (resource_norm.code, resource_norm.name, resource_norm.pdf_link, id)
    )
    db.commit()
    return {**resource_norm.dict(), "id": id}

@router.delete("/resource-norms/{id}")
async def delete_resource_norm(
    id: int,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM resource_norms WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Resource norm not found")
    cursor.execute("DELETE FROM resource_norms WHERE id = ?", (id,))
    db.commit()
    return {"message": "Resource norm deleted"}

# MA'LUMOTNOMA
@router.post("/reference-docs", response_model=ReferenceResponse)
async def create_reference(
    reference: ReferenceCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO reference_docs (name, pdf_link) VALUES (?, ?)",
        (reference.name, reference.pdf_link)
    )
    db.commit()
    return {**reference.dict(), "id": cursor.lastrowid}

@router.get("/reference-docs", response_model=List[ReferenceResponse])
async def get_references(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reference_docs")
    items = cursor.fetchall()
    return [{"id": item["id"], "name": item["name"], "pdf_link": item["pdf_link"]} for item in items]

@router.put("/reference-docs/{id}", response_model=ReferenceResponse)
async def update_reference(
    id: int,
    reference: ReferenceCreate,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reference_docs WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Reference not found")
    cursor.execute(
        "UPDATE reference_docs SET name = ?, pdf_link = ? WHERE id = ?",
        (reference.name, reference.pdf_link, id)
    )
    db.commit()
    return {**reference.dict(), "id": id}

@router.delete("/reference-docs/{id}")
async def delete_reference(
    id: int,
    current_user: dict = Depends(get_current_admin),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reference_docs WHERE id = ?", (id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Reference not found")
    cursor.execute("DELETE FROM reference_docs WHERE id = ?", (id,))
    db.commit()
    return {"message": "Reference deleted"}