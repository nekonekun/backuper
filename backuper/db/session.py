from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


def get_async_session(postgres_url: str):
    engine = create_async_engine(postgres_url)
    async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    return async_session
