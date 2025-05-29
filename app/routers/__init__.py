from fastapi import APIRouter
from app.routers import items, lists

router = APIRouter()
router.include_router(items.router,  tags=["items"])
router.include_router(lists.router,  tags=["lists"])