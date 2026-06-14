import typer
import asyncio
from src.notes.service import set_note, get_all_notes, delete_note, get_all_by_tags, update_note
from rich.console import Console
from rich.table import Table

console = Console()

note_app = typer.Typer(help="Управление заметками")


@note_app.command(name="add")
def add(
    title: str,
    content: str,
    tag: str = typer.Option(None, "--category", "-c", help="Тег"),
):
    capi_title, capi_content, capi_tag = (
        title.capitalize(),
        content.capitalize(),
        tag.capitalize() if tag else None,
    )
    asyncio.run(set_note(title=capi_title, text=capi_content, tag=capi_tag))
    console.print(f"Успешно добавлена задача {title}✅")

@note_app.command(name="edit")
def edit_note(
    title: str,
    ed_content: str = typer.Option(None, "--text", "-tx", help="Обновление текста"),
    ed_tag: str = typer.Option(None, "--tag", "-tg", help="Обновлние тега"),
    ed_title: str = typer.Option(None, "--title", "-tl", help="Обновление загаловка")
):
    capi_title, egcapi_content, egcapi_tag, egcapi_title = (
        title.capitalize(),
        ed_content.capitalize() if ed_content else None,
        ed_tag.capitalize() if ed_tag else None,
        ed_title.capitalize() if ed_title else None
    )
    asyncio.run(update_note(title = capi_title, edcontent=ed_content, edtag=ed_tag, edtitle=ed_title))
    console.print(f"Заметка {title} успешно изменена✅")



@note_app.command(name="del")
def delete(id: str):
    elements = [item.strip() for item in id.split(",")]
    for element in elements:
        asyncio.run(delete_note(id=int(element)))
        console.print(f"Задача с ID {element} была успешно удалена!✅")


@note_app.command(name="listbytag")
def list_by_tag(tag: str):
    capi_tag = tag.capitalize()
    notes = asyncio.run(get_all_by_tags(capi_tag))
    if not notes:
        console.print("[bold yellow]Заметок по этому тегу нет![/bold yellow]")
        return
    table = Table(
        title=f"Список заметок по тегу {capi_tag}",
        title_style="bold magenta",
        show_lines=True,
    )
    table.add_column("Заголовок", style="bold green", justify="center")
    table.add_column("Описание", style="white")

    for note in notes:
        table.add_row(note.title, note.content)
    console.print(table)


@note_app.command(name="list")
def list_notes():
    notes = asyncio.run(get_all_notes())
    if not notes:
        console.print("[bold yellow]БД пуста![/bold yellow]")
        return
    table = Table(
        title="Список всех заметок", title_style="bold magenta", show_lines=True
    )
    table.add_column("ID", style="dim cyan", justify="center")
    table.add_column("Заголовок", style="bold green")
    table.add_column("Описание", style="white")
    table.add_column("Тег", style="italic blue")
    table.add_column("Создана", style="white")

    for note in notes:
        time_str = note.created_at.strftime("%d.%m.%Y %H:%M")
        cat = note.tag if note.tag else "-"
        table.add_row(str(note.id), note.title, note.content, cat, time_str)
    console.print(table)






