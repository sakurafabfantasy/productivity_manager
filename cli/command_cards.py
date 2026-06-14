import typer
import asyncio
from src.flashcards.service import add_word, cards_list, del_all, choosen_words, change_card_status, delete_card, sample_cards, choosen_words_tr
from rich.console import Console
from src.flashcards.get_tr import translate
from rich.table import Table
import re

console = Console()
cards_app = typer.Typer(help="Анки")

@cards_app.command(name="add", help="Введите слово и язык на который вы хотите его перевести, пример: add 'яблоко' 'испанский' ")
def add_card(word: str, lang: str):
    output = translate(word, lang)
    try:
        outword, outlang2, outlang1 = output.strip().lower().split(",")
    except ValueError:
        console.print("⛔️")
        return
    
    capi_word = word.capitalize()
    capi_lang = outlang1.capitalize()
    capi_trword = outword.capitalize()
    is_added = asyncio.run(add_word(trword=capi_trword, lang=capi_lang, word=capi_word))
    console.print(f"{word} на {outlang2} -> {outword}\nСлово успешно добавлено в список✅") 
@cards_app.command(name="list")
def show_cards():
    
    all_cards = asyncio.run(cards_list())
    table = Table(title = "Все карточки", style = "bold magenta", show_lines = True)
    table.add_column("ID", style = "dim cyan")
    table.add_column("Слово", style = "bold white")
    table.add_column("Перевод", style = "bold white")
    table.add_column("Язык", style = "italic blue")
    table.add_column("Статус в памяти", style = "bold white")
    table.add_column("Будет доступна после", style = "dim cyan")
    for card in all_cards:
        table.add_row(str(card.id), card.word, card.trword, card.language, str(card.status), str(card.available_after))

    console.print(table) 


@cards_app.command(name="rmrf")
def rmrf():
    asyncio.run(del_all())
    console.print("Всё удалено✅")


@cards_app.command(name="study", help="Изучение новых слов")
def study():
    languages = asyncio.run(cards_list())
    if not languages:
        console.print("[bold red]БД ПУСТА[/bold red]")
        return
    
    table = Table(title = "Все языки из БД", style = "bold yellow", show_lines=True)
    table.add_column("Язык", style = "white")

    seen_lang = set()

    for lang in languages:
        if lang.language not in seen_lang:
            table.add_row(lang.language)
            seen_lang.add(lang.language)

    console.print(table)

    choosen_lang = str(input(f"Выберите язык\n")).capitalize()

    usr_words = asyncio.run(choosen_words(choosen_lang))
    
    if not usr_words:
        console.print("[bold green]Отлично, на сегодня все слова по этому языку повторены! [/bold green]")
        return
    
    for card in usr_words:
        console.print(card, style = "bold white")
        mark = int(input(f"Оцените на сколько вы знаете это слово:\n4 - помню отлично\n3 - помню хорошо, но думал 10сек\n2 - помню с трудом\n1 - вообще не помню\n"))
        asyncio.run(change_card_status(word=card, num=mark))
        usr_translates = asyncio.run(choosen_words_tr(card, choosen_lang))
        console.print(f"Перевод {card} -> {usr_translates}")
        
    console.print(f"Все слова по языку {choosen_lang} повторены!✅")
        
@cards_app.command(name="del", help="Введите карточку или карточки через запятые которые хотите удалить")
def delete_card_by_id(id: str):
    elements = [item.strip() for item in id.split(",")]

    for element in elements:
        asyncio.run(delete_card(id=int(element)))
        console.print(f"Карточка с ID {element} была успешно удалена!✅")


@cards_app.command(name="sample")
def add_sample():
    asyncio.run(sample_cards())
    console.print("✅")


        
