from fastapi import APIRouter
from app.routes import items, lists

router = APIRouter()
router.include_router(items.router, prefix="/items", tags=["items"])
router.include_router(lists.router, prefix="/lists", tags=["lists"])