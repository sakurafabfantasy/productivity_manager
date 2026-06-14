from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from database.models import Base, Notes, Tasks


engine = create_async_engine(url="sqlite+aiosqlite:////home/sakura/Рабочий стол/projects/productivity_manager/db.sqlite3")
async_session = async_sessionmaker(engine)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)