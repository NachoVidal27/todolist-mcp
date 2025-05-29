from fastapi import FastAPI
from app.routers import router as api_router
from app.mcp import router as mcp_router
from app.models import Base
from app.database import engine
from dotenv import load_dotenv
from fastapi_mcp import FastApiMCP

load_dotenv() 

app = FastAPI(title="TodoList API with MCP Server")

mcp = FastApiMCP(app)

mcp.mount()

app.include_router(api_router, prefix="/api")
app.include_router(mcp_router, prefix="/mcp")

Base.metadata.create_all(bind=engine)

mcp.setup_server()