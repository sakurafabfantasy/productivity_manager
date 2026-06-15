from database.models import Tasks
from database.connection import async_session
from sqlalchemy import select, delete
from datetime import datetime, timedelta

async def set_task(title: str, tag: str | None = None, is_completed: bool = False):
    async with async_session() as session:
        task = await session.scalar(select(Tasks).where(Tasks.title == title))
        if not task:
            session.add(Tasks(title=title, tag=tag, is_completed=is_completed))
            await session.commit()


async def get_all_tasks():
    async with async_session() as session:
        result = await session.execute(select(Tasks))
        return result.scalars().all()


async def complete(id: int):
    async with async_session() as session:
        task = await session.scalar(select(Tasks).where(Tasks.id == id))
        if task:
            task.is_completed = True
            await session.commit()


async def delete_task(id: int):
    async with async_session() as session:
        task = await session.execute(delete(Tasks).where(Tasks.id == id))
        await session.commit()


async def show_by_tag(tag: str):
    async with async_session() as session:
        result = await session.execute(select(Tasks).where(Tasks.tag == tag))
        if result:
            return result.scalars().all()
        
async def del_all():
    async with async_session() as session:
        await session.execute(delete(Tasks))
        await session.commit()

async def archive_date(id: int):
    async with async_session() as session:
        result = await session.scalar(select(Tasks).where(Tasks.id == id))
        if result:
            result.expiring_date = datetime.now() + timedelta(days=30)
        await session.commit()
            