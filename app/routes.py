from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import get_items, create_item, update_item, delete_item
from models import TodoItem, TodoItemCreate, TodoItemUpdate

router = APIRouter()


@router.get("/items/", response_model=List[TodoItem])
def read_items(db: Session = Depends(get_db)):
    return get_items(db)


@router.post("/items/", response_model=TodoItem)
def create_new_item(item: TodoItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)


@router.put("/items/{item_id}", response_model=TodoItem)
def update_existing_item(item_id: int, item: TodoItemUpdate, db: Session = Depends(get_db)):
    updated = update_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated


@router.delete("/items/{item_id}")
def delete_existing_item(item_id: int, db: Session = Depends(get_db)):
    deleted = delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}
