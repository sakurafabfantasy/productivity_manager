from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from database.models import BaseModels, BaseChoice


engine_main = create_async_engine(url="sqlite+aiosqlite:////home/sakura/Рабочий стол/projects/productivity_manager/maindb.sqlite3")
engine_settings = create_async_engine(url="sqlite+aiosqlite:////home/sakura/Рабочий стол/projects/productivity_manager/settingsdb.sqlite3")

async_session_main = async_sessionmaker(engine_main)
async_session_settings = async_sessionmaker(engine_settings)

async def async_main():
    async with engine_main.begin() as conn:
        await conn.run_sync(BaseModels.metadata.create_all)
    async with engine_settings.begin() as conn:
        await conn.run_sync(BaseChoice.metadata.create_all)