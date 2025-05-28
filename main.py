from fastapi import FastAPI
from app.api import router as api_router
from app.mcp import router as mcp_router
from app.models import Base
from app.database import engine

app = FastAPI(title="TodoList API with MCP Server")

# API principal bajo el prefijo /api
app.include_router(api_router, prefix="/api")

# MCP Server bajo el prefijo /mcp
app.include_router(mcp_router, prefix="/mcp")

Base.metadata.create_all(bind=engine)