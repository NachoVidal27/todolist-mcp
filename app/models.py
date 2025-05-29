from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from typing import Optional
from pydantic import BaseModel
from app.database import Base

# SQLAlchemy ORM models

class ListORM(Base):
    __tablename__ = "lists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    items = relationship("TodoItemORM", back_populates="list", cascade="all, delete-orphan")


class TodoItemORM(Base):
    __tablename__ = "todoitems"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    list_id = Column(Integer, ForeignKey("lists.id"))

    list = relationship("ListORM", back_populates="items")


# Pydantic models

class ListBase(BaseModel):
    name: str

class ListCreate(ListBase):
    pass

class ListUpdate(BaseModel):
    name: Optional[str] = None

class List(ListBase):
    id: int

    class Config:
        orm_mode = True


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


# Claude prompt models 

class PromptRequest(BaseModel):
    prompt: str

class ClaudeResponse(BaseModel):
    response: str
