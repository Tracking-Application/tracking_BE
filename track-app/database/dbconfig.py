from sqlalchemy.ext.asyncio import create_async_engine
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env if present

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("35.174.7.151")
DB_PORT = os.getenv("DB_PORT") or 5432
DB_NAME = os.getenv("POSTGRES_DB")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)


