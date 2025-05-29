from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud import get_items, create_item, update_item, delete_item
from app.models import TodoItem, TodoItemCreate, TodoItemUpdate

router = APIRouter(prefix="/items")

@router.get("/", response_model=List[TodoItem])
def read_items(db: Session = Depends(get_db)):
    return get_items(db)
  
@router.get("/{item_id}", response_model=TodoItem)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(TodoItemORM).filter(TodoItemORM.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=TodoItem)
def create_new_item(item: TodoItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)

@router.put("/{item_id}", response_model=TodoItem)
def update_existing_item(item_id: int, item: TodoItemUpdate, db: Session = Depends(get_db)):
    updated = update_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/{item_id}")
def delete_existing_item(item_id: int, db: Session = Depends(get_db)):
    deleted = delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}
