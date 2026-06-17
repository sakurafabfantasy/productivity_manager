from database.models import Notes
from database.connection import async_session_main
from sqlalchemy import select, delete


async def set_note(title: str, text: str, tag: str | None = None):
    async with async_session_main() as session:
        note = await session.scalar(select(Notes).where(Notes.title == title))
        if not note:
            session.add(Notes(title=title, content=text, tag=tag))
            await session.commit()


async def delete_note(id: int):
    async with async_session_main() as session:
        await session.execute(delete(Notes).where(Notes.id == id))
        await session.commit()


async def get_all_notes():
    async with async_session_main() as session:
        result = await session.execute(select(Notes))
        return result.scalars().all()


async def get_all_by_tags(tag: str):
    async with async_session_main() as session:
        result = await session.execute(select(Notes).where(Notes.tag == tag))
        return result.scalars().all()

async def update_note(title: str, edcontent: str | None = None, edtag: str | None = None, edtitle: str | None = None):
    async with async_session_main() as session:
        note = await session.scalar(select(Notes).where(Notes.title == title))
        if note:
            if edcontent is not None:
                note.content = edcontent
            elif edtag is not None:
                note.tag = edtag
            elif edtitle is not None:
                note.title = edtitle
            else:
                return
            await session.commit()

async def info_note(id: int):
    async with async_session_main() as session:
        result = await session.scalar(select(Notes).where(Notes.id == id))
        if result:
            return result




            


