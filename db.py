from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB

url = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(url,echo=True)
async_session = async_sessionmaker(engine,expire_on_commit=False)

async def get_session():
    async with async_session() as session:
        yield session
