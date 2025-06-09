from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db import create_db_and_tables

@asynccontextmanager
async def lifespan(app:FastAPI):
        try:
            print("Lifespan: Iniciando aplicación...")
            await create_db_and_tables()
            print("Lifespan: Fase de inicio completada.")
            yield
            print("Lifespan: Cerrando aplicación...")
        finally:
            pass