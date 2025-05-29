from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud import (
    get_items, create_item, update_item, delete_item,
    get_lists, create_list, update_list, delete_list
)
from app.models import (
    TodoItem, TodoItemCreate, TodoItemUpdate,
    List, ListCreate, ListUpdate
)

router = APIRouter()

# TodoItems endpoints

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


# Lists endpoints

@router.get("/lists/", response_model=List[List])
def read_lists(db: Session = Depends(get_db)):
    return get_lists(db)

@router.post("/lists/", response_model=List)
def create_new_list(list_create: ListCreate, db: Session = Depends(get_db)):
    return create_list(db, list_create)

@router.put("/lists/{list_id}", response_model=List)
def update_existing_list(list_id: int, list_update: ListUpdate, db: Session = Depends(get_db)):
    updated = update_list(db, list_id, list_update)
    if not updated:
        raise HTTPException(status_code=404, detail="List not found")
    return updated

@router.delete("/lists/{list_id}")
def delete_existing_list(list_id: int, db: Session = Depends(get_db)):
    deleted = delete_list(db, list_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="List not found")
    return {"message": "List deleted"}
