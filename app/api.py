from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List as ListType
from app.database import get_db
from app.crud import (
    get_items, create_item, update_item, delete_item,
    complete_item, create_item_in_list,
    get_lists, create_list, update_list, delete_list
)
from app.models import (
    TodoItem, TodoItemCreate, TodoItemUpdate,
    List, ListCreate, ListUpdate, ListORM
)

router = APIRouter()

##Items

@router.get("/items/", response_model=ListType[TodoItem])
def read_items(db: Session = Depends(get_db)):
    return get_items(db)


@router.post("/items/", response_model=TodoItem)
def create_new_item(item: TodoItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)

@router.post("/lists/{list_id}/items", response_model=TodoItem)
def create_item_in_specific_list(list_id: int, item: TodoItemCreate, db: Session = Depends(get_db)):
    # Verificar que la lista existe usando el modelo ORM
    lista = db.query(ListORM).filter(ListORM.id == list_id).first()
    if not lista:
        raise HTTPException(status_code=404, detail="List not found")
    
    return create_item_in_list(db, list_id, item)   

@router.put("/items/{item_id}", response_model=TodoItem)
def update_existing_item(item_id: int, item: TodoItemUpdate, db: Session = Depends(get_db)):
    updated = update_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.patch("/items/{item_id}/complete", response_model=TodoItem)
def complete_existing_item(item_id: int, db: Session = Depends(get_db)):
    completed = complete_item(db, item_id)
    if not completed:
        raise HTTPException(status_code=404, detail="Item not found")
    return completed

@router.delete("/items/{item_id}")
def delete_existing_item(item_id: int, db: Session = Depends(get_db)):
    deleted = delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}


## Lists
@router.post("/lists/", response_model=List)
def create_new_list(lista: ListCreate, db: Session = Depends(get_db)):
    return create_list(db, lista)

@router.get("/lists/", response_model=ListType[List])
def read_lists(db: Session = Depends(get_db)):
    return get_lists(db)



@router.put("/lists/{list_id}", response_model=List)
def update_existing_list(list_id: int, lista: ListUpdate, db: Session = Depends(get_db)):
    updated = update_list(db, list_id, lista)
    if not updated:
        raise HTTPException(status_code=404, detail="List not found")
    return updated

@router.delete("/lists/{list_id}")
def delete_existing_list(list_id: int, db: Session = Depends(get_db)):
    deleted = delete_list(db, list_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="List not found")
    return {"message": "List deleted"}