from database.models import UserSettings
from database.connection import async_session_settings
from sqlalchemy import select

async def set_setting(tg_id: int, choice: str):
    async with async_session_settings() as session:
        result = await session.scalar(select(UserSettings).where(UserSettings.tg_id == tg_id))
        if not result:
            session.add(UserSettings(tg_id=tg_id, setting=choice))
            await session.commit()
        else:
            result.setting = choice
            await session.commit()

async def find_mode(tg_id: int):
    async with async_session_settings() as session:
        result = await session.scalar(select(UserSettings).where(UserSettings.tg_id == tg_id))
        if result:
            return result