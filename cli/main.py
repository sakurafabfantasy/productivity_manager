import asyncio
from cli.command_notes import note_app
from cli.command_tasks import task_app
from cli.command_cards import cards_app
from database.connection import async_main
import typer

app = typer.Typer(help="fdffd")


@app.callback()
def init_db():
    asyncio.run(async_main())


app.add_typer(note_app, name="notes")
app.add_typer(task_app, name="tasks")
app.add_typer(cards_app, name="cards")


if __name__ == "__main__":
    app()
