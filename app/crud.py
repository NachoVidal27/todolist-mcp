from sqlalchemy.orm import Session
from app.models import (
    TodoItemORM, TodoItemCreate, TodoItemUpdate,
    ListORM, ListCreate, ListUpdate
)

# TodoItem CRUD

def get_items(db: Session):
    return db.query(TodoItemORM).all()

def create_item(db: Session, item: TodoItemCreate):
    db_item = TodoItemORM(
        description=item.description,
        completed=item.completed,
        list_id=item.list_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# NUEVA: Crear ítem en una lista específica
def create_item_in_list(db: Session, list_id: int, item: TodoItemCreate):
    db_item = TodoItemORM(
        description=item.description,
        completed=item.completed if item.completed is not None else False,
        list_id=list_id  # Forzamos el list_id del parámetro
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
        db_item.description = item.description
    if item.completed is not None:
        db_item.completed = item.completed
    if item.list_id is not None:
        db_item.list_id = item.list_id
    db.commit()
    db.refresh(db_item)
    return db_item

# NUEVA: Completar un ítem (marcar como terminado)
def complete_item(db: Session, item_id: int):
    db_item = db.query(TodoItemORM).filter(TodoItemORM.id == item_id).first()
    if not db_item:
        return None
    db_item.completed = True
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


# List CRUD

def create_list(db: Session, list_create: ListCreate):
    db_list = ListORM(name=list_create.name)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

def get_lists(db: Session):
    return db.query(ListORM).all()

def get_list_by_id(db: Session, list_id: int):
    return db.query(ListORM).filter(ListORM.id == list_id).first()

def update_list(db: Session, list_id: int, update_data: ListUpdate):
    db_list = db.query(ListORM).filter(ListORM.id == list_id).first()
    if not db_list:
        return None
    if update_data.name is not None:
        db_list.name = update_data.name
    db.commit()
    db.refresh(db_list)
    return db_list

def delete_list(db: Session, list_id: int):
    db_list = db.query(ListORM).filter(ListORM.id == list_id).first()
    if not db_list:
        return False
    db.delete(db_list)
    db.commit()
    return True