import typer
import asyncio
from src.tasks.service import set_task, get_all_tasks, complete, delete_task, show_by_tag, del_all
from rich.console import Console
from rich.table import Table

console = Console()
task_app = typer.Typer(help="Управление задачами")
translation = {"True": "Завершена", "False": "Незавершена"}

@task_app.command(name="add")
def add_task(
    title: str, tag: str = typer.Option(None, "--category", "-c", help="Добавьте тег")
):
    capi_title, capi_tag = title.capitalize(), tag.capitalize() if tag else None

    asyncio.run(set_task(title=capi_title, tag=capi_tag))
    console.print(
        f"Задача {title} успешно добавлена в БД! Напишите note task list для просмотра списка"
    )


@task_app.command(name="list")
def get_tasks():
    tasks = asyncio.run(get_all_tasks())
    global translation

    if not tasks:
        console.print("[bold yellow]БД пуста![/bold yellow]")
        return
    table = Table(
        title="Список всех задач", title_style="bold magenta", show_lines=True
    )
    table.add_column("ID", style="dim cyan", justify="center")
    table.add_column("Задача", style="bold green")
    table.add_column("Выполнена ли", style="white")
    table.add_column("Тег", style="italic blue")
    table.add_column("Дата создания", style="white")

    is_header = False
    sorted_tasks = sorted(tasks, key=lambda x: x.is_completed)
    for task in sorted_tasks:
        time_str = task.created_at.strftime("%d.%m.%Y %H:%M")
        cat = task.tag if task.tag else "-"

        if not task.is_completed:
            table.add_row(
                str(task.id),
                task.title,
                translation[str(task.is_completed)],
                cat,
                time_str,
            )
            continue
        else:
            if is_header == False:
                table.add_row("Архив", style="dim red")
                is_header = True

            table.add_row(
                str(task.id),
                task.title,
                translation[str(task.is_completed)],
                cat,
                time_str,
            )

    console.print(table)


@task_app.command(name="complete")
def make_task_complete(id: int):
    asyncio.run(complete(id = id))
    console.print(
        f"Задача с ID {id} отмечена как завершённая!Напишите note task list для просмотра списка"
    )


@task_app.command(name="del", help="Введите задачу или задачи которые хотите удалить через запятую")
def task_delete(id: str):
    elements = [item.strip() for item in id.split(",")]
    for element in elements:
        asyncio.run(delete_task(id=int(element)))
        console.print(f"Задача с ID {element} была успешно удалена!✅")

@task_app.command(name="listbytag")
def listag(tag: str):
    capi_tag = tag.capitalize()
    tasks = asyncio.run(show_by_tag(tag=capi_tag))
    global translation

    if not tasks:
        console.print(f"В БД нету задач с тегом {capi_tag}")
        return
    
    table = Table(title=f"Список задач по тегу {capi_tag}", style="bold", show_lines=True)
    table.add_column("Задача", style = "bold green", justify="center")
    table.add_column("Выполнена ли", style = "white")
    
    for task in tasks:
        table.add_row(task.title, translation[str(task.is_completed)])

    console.print(table)

@task_app.command("rmrf")
def rmrf():
    asyncio.run(del_all())
    console.print("Всё успешно удалено✅")

