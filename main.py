from fastapi import FastAPI
from app.routers import items, lists
from app.mcp import router as mcp_router
from app.models import Base
from app.database import engine

app = FastAPI(title="TodoList API with MCP Server")

# Incluye los routers modulares para items y listas bajo el prefijo /api
app.include_router(items.router, prefix="/api/items", tags=["items"])
app.include_router(lists.router, prefix="/api/lists", tags=["lists"])

# MCP Server bajo el prefijo /mcp
app.include_router(mcp_router, prefix="/mcp", tags=["mcp"])

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)
