from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from fast_api.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
