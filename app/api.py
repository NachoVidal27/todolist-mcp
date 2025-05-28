from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud import (
    get_items, create_item, update_item, delete_item,
    get_listas, create_lista, update_lista, delete_lista
)
from app.models import (
    TodoItem, TodoItemCreate, TodoItemUpdate,
    Lista, ListaCreate, ListaUpdate
)

router = APIRouter()

##Items

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


## Listas
@router.post("/listas/", response_model=Lista)
def create_new_list(lista: ListaCreate, db: Session = Depends(get_db)):
    return create_lista(db, lista)

@router.get("/listas/", response_model=List[Lista])
def read_lists(db: Session = Depends(get_db)):
    return get_listas(db)

@router.put("/listas/{lista_id}", response_model=Lista)
def update_existing_list(lista_id: int, lista: ListaUpdate, db: Session = Depends(get_db)):
    updated = update_lista(db, lista_id, lista)
    if not updated:
        raise HTTPException(status_code=404, detail="Lista not found")
    return updated

@router.delete("/listas/{lista_id}")
def delete_existing_list(lista_id: int, db: Session = Depends(get_db)):
    deleted = delete_lista(db, lista_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Lista not found")
    return {"message": "Lista deleted"}
