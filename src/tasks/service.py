from database.models import Tasks
from database.connection import async_session_main
from sqlalchemy import select, delete
from datetime import datetime, timedelta

async def set_task(title: str, tg_id: int, tag: str | None = None, is_completed: bool = False):
    async with async_session_main() as session:
        task = await session.scalar(select(Tasks).where(Tasks.title == title, Tasks.user_id == tg_id))
        if not task:
            session.add(Tasks(title=title, tag=tag, is_completed=is_completed, user_id=tg_id))
            await session.commit()


async def get_all_tasks(tg_id: int):
    async with async_session_main() as session:
        result = await session.execute(select(Tasks).where(Tasks.user_id == tg_id))
        return result.scalars().all()


async def complete(id: int):
    async with async_session_main() as session:
        task = await session.scalar(select(Tasks).where(Tasks.id == id))
        if task:
            task.is_completed = True
            await session.commit()


async def delete_task(id: int):
    async with async_session_main() as session:
        task = await session.execute(delete(Tasks).where(Tasks.id == id))
        await session.commit()


async def show_by_tag(tag: str, tg_id: int):
    async with async_session_main() as session:
        result = await session.execute(select(Tasks).where(Tasks.tag == tag, Tasks.user_id == tg_id))
        if result:
            return result.scalars().all()
        
async def del_all(tg_id: int):
    async with async_session_main() as session:
        await session.execute(delete(Tasks).where(Tasks.user_id == tg_id))
        await session.commit()

async def archive_date(id: int):
    async with async_session_main() as session:
        result = await session.scalar(select(Tasks).where(Tasks.id == id))
        if result:
            result.expiring_date = datetime.now() + timedelta(days=30)
        await session.commit()


async def add_sample(tg_id: int):
    async with async_session_main() as session:
        tasks_sample = [
            "Сделать уроки, школа",
            "Поесть бургеры",
            "Погулять с патриком",
            "Погулять в чернобыле",
            "Убраться, дом",
            "Собрать лего, досуг"
        ]
        for task in tasks_sample:
            try:
                title, tag = task.strip().capitalize().split(",")
            except ValueError:
                title = task.strip().capitalize()
            matched = await session.scalar(select(Tasks).where(Tasks.title == title, Tasks.user_id == tg_id))
            if not matched:
                await set_task(title=title, tag=tag, tg_id=tg_id)
        await session.commit()


async def info_abt_task(title: str, tg_id: int):
    async with async_session_main() as session:
        result = await session.scalar(select(Tasks).where(Tasks.title == title, Tasks.user_id == tg_id))
        if result: 
            return result

async def search_id(id: int):
    async with async_session_main() as session:
        result = await session.scalar(select(Tasks).where(Tasks.id == id))
        if result:
            return result.title