import uvicorn
import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy import text

from app.database import db_helper
from app.config import settings
from app.routers.auth import router as auth_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    async for session in db_helper.session_getter():
        result = await session.execute(text("SELECT 1"))
        print(result.scalar())

    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router, prefix="/auth")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
