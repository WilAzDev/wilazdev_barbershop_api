from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.conf import get_settings
from app import models

settings = get_settings()

DATABASE_URL = settings.db_url
async_engine = create_async_engine(DATABASE_URL, echo=True,future=True)
        
        
async def create_db_and_tables():
    print("START_EVENTS: Intentando crear tablas...")
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("START_EVENTS: Creación de tablas completada (o ya existían).")
        
async def get_async_session() -> AsyncGenerator[AsyncSession,None]:
    async with AsyncSession(async_engine) as session:
        yield session