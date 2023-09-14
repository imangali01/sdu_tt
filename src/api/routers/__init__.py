from fastapi import APIRouter, Depends

from .trello.router import router as trello_router
from .telegram.router import router as telegram_router



router = APIRouter(
    prefix='/api',
    include_in_schema=True
)

router.include_router(trello_router)
router.include_router(telegram_router)
