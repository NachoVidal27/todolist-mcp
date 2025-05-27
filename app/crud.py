from sqlalchemy.orm import Session
from app.models import TodoItemDB  # Modelo SQLAlchemy de la tabla
from app.models import TodoItemCreate, TodoItemUpdate  # Pydantic schemas en models.py 


def get_items(db: Session):
    return db.query(TodoItemDB).all()

def get_item(db: Session, item_id: int):
    return db.query(TodoItemDB).filter(TodoItemDB.id == item_id).first()

def create_item(db: Session, item_create: TodoItemCreate):
    db_item = TodoItemDB(
        description=item_create.description,
        list_id=item_create.list_id,
        completed=item_create.completed,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item_update: TodoItemUpdate):
    db_item = db.query(TodoItemDB).filter(TodoItemDB.id == item_id).first()
    if not db_item:
        return None
    if item_update.description is not None:
        db_item.description = item_update.description
    if item_update.completed is not None:
        db_item.completed = item_update.completed
    if item_update.list_id is not None:
        db_item.list_id = item_update.list_id
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(TodoItemDB).filter(TodoItemDB.id == item_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item
