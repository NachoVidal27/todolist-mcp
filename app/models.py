from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from typing import Optional
from pydantic import BaseModel
from app.database import Base  

# modelos orm sqlalchemy


class ListaORM(Base):
    __tablename__ = "listas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)

    items = relationship("TodoItemORM", back_populates="lista", cascade="all, delete-orphan")


class TodoItemORM(Base):
    __tablename__ = "todoitems"
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, index=True)
    completado = Column(Boolean, default=False)
    lista_id = Column(Integer, ForeignKey("listas.id"))

    lista = relationship("ListaORM", back_populates="items")



# Modelos Pydantic (Schemas)

class ListaBase(BaseModel):
    nombre: str

class ListaCreate(ListaBase):
    pass

class ListaUpdate(BaseModel):
    nombre: Optional[str] = None

class Lista(ListaBase):
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



# modelos Claude


class PromptRequest(BaseModel):
    prompt: str

class ClaudeResponse(BaseModel):
    response: str
