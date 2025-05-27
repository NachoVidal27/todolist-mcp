from sqlalchemy import Column, Integer, String, Boolean
from typing import Optional
from pydantic import BaseModel
from app.database import Base  # Importamos Base único desde database.py

# Modelos Pydantic (schemas)

class TodoItemBase(BaseModel):
    description: str
    completed: bool = False
    list_id: int

class TodoItemCreate(TodoItemBase):
    pass

class TodoItemUpdate(BaseModel):
    description: Optional[str] = None
    completed: Optional[bool] = None
    list_id: Optional[int] = None

class TodoItem(TodoItemBase):
    id: int

    class Config:
        orm_mode = True

class PromptRequest(BaseModel):
    prompt: str

class ClaudeResponse(BaseModel):
    response: str

# Modelo SQLAlchemy (ORM)

class TodoItemDB(Base):
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
