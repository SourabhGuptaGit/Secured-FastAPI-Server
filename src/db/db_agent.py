from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine

from src.utils.config import settings


engine = AsyncEngine(
    create_engine(
        url=settings.DATABASE_URL,
        echo=True
    )
)

async def init_db():
    async with engine.begin() as conn:
        from src.books.models import Books
        await conn.run_sync(SQLModel.metadata.create_all)
        # statement = text("SELECT 'Hello';")
        
        # result = await conn.execute(statement)
        
        # print(result.all())