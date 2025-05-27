from app.database import Base, engine
from app.models import TodoItemDB

Base.metadata.create_all(bind=engine)

