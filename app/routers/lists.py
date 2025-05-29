from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from typing import List as TypingList
from app.database import get_db
from app.crud import get_lists, create_list, update_list, delete_list
from app.models import List, ListCreate, ListUpdate

router = APIRouter(prefix="/lists")

@router.get("/", response_model=TypingList[List])
def read_lists(db: Session = Depends(get_db)):
    return get_lists(db)

@router.get("/{list_id}", response_model=List)
def read_list(list_id: int, db: Session = Depends(get_db)):
    db_list = get_list_by_id(db, list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    return db_list

@router.post("/", response_model=List)
def create_new_list(list_create: ListCreate, db: Session = Depends(get_db)):
    return create_list(db, list_create)

@router.put("/{list_id}", response_model=List)
def update_existing_list(list_id: int, list_update: ListUpdate, db: Session = Depends(get_db)):
    updated = update_list(db, list_id, list_update)
    if not updated:
        raise HTTPException(status_code=404, detail="List not found")
    return updated

@router.delete("/{list_id}")
def delete_existing_list(list_id: int, db: Session = Depends(get_db)):
    deleted = delete_list(db, list_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="List not found")
    return {"message": "List deleted"}
