from sqlalchemy.orm import Session
from app.models import (
    TodoItemORM, TodoItemCreate, TodoItemUpdate,
    ListaORM, ListaCreate, ListaUpdate
)

#TodoItem


def get_items(db: Session):
    return db.query(TodoItemORM).all()

def create_item(db: Session, item: TodoItemCreate):
    db_item = TodoItemORM(
        descripcion=item.description,
        completado=item.completed,
        lista_id=item.list_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: TodoItemUpdate):
    db_item = db.query(TodoItemORM).filter(TodoItemORM.id == item_id).first()
    if not db_item:
        return None
    if item.description is not None:
        db_item.descripcion = item.description
    if item.completed is not None:
        db_item.completado = item.completed
    if item.list_id is not None:
        db_item.lista_id = item.list_id
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(TodoItemORM).filter(TodoItemORM.id == item_id).first()
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True


#Lista


def create_lista(db: Session, lista: ListaCreate):
    db_lista = ListaORM(nombre=lista.nombre)
    db.add(db_lista)
    db.commit()
    db.refresh(db_lista)
    return db_lista

def get_listas(db: Session):
    return db.query(ListaORM).all()

def get_lista_by_id(db: Session, lista_id: int):
    return db.query(ListaORM).filter(ListaORM.id == lista_id).first()

def update_lista(db: Session, lista_id: int, update_data: ListaUpdate):
    db_lista = db.query(ListaORM).filter(ListaORM.id == lista_id).first()
    if not db_lista:
        return None
    if update_data.nombre is not None:
        db_lista.nombre = update_data.nombre
    db.commit()
    db.refresh(db_lista)
    return db_lista

def delete_lista(db: Session, lista_id: int):
    db_lista = db.query(ListaORM).filter(ListaORM.id == lista_id).first()
    if not db_lista:
        return False
    db.delete(db_lista)
    db.commit()
    return True
