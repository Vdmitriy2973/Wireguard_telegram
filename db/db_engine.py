from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from .db_conf import db_settings
from .db_models import Base

async_engine = create_async_engine(
    url=db_settings.database_url_psycopg
)

async_session  = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine,class_=AsyncSession)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
