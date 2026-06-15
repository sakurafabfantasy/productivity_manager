from database.models import Flashcards
from database.connection import async_session
from sqlalchemy import select, delete
from datetime import timedelta, datetime

async def add_word(trword: str, lang: str, word: str):
    async with async_session() as session:
        slovo = await session.scalar(select(Flashcards).where(Flashcards.word == word))
        if not slovo:
            session.add(Flashcards(word=trword, language=lang, trword=word))
            await session.commit()

async def cards_list():
    async with async_session() as session:
        query = select(Flashcards).distinct()
        result = await session.execute(query)
        return result.scalars().all()

async def del_all():
    async with async_session() as session:
        await session.execute(delete(Flashcards))
        await session.commit()



async def choosen_words(lang: str):
    async with async_session() as session:
        current_time = datetime.now()
        query = (
            select(Flashcards.word)
            .where(
                Flashcards.language == lang,
                Flashcards.available_after <= current_time  
            )
        )
        result = await session.execute(query)
        return result.scalars().all()
    
async def choosen_words_tr(word: str, lang: str):
    async with async_session() as session:
        query = (
            select(Flashcards.trword)
            .where(
                Flashcards.language == lang,
                Flashcards.word == word
            )
        )
        result = await session.execute(query)
        return result.scalar()



async def change_card_status(word, num: int):
    async with async_session() as session:
        
        card = await session.scalar(select(Flashcards).where(Flashcards.word == word))
        if card:
            card.status = num
            match num:
                case 1:
                    card.available_after = datetime.now() + timedelta(days=1)
                case 2:
                    card.available_after = datetime.now() + timedelta(days=3)
                case 3:
                    card.available_after = datetime.now() + timedelta(days=7)
                case 4:
                    card.available_after = datetime.now() + timedelta(days=14)
                case 5:
                    card.available_after = datetime.now() + timedelta(days=30)
            await session.commit()




        


async def delete_card(id: int):
    async with async_session() as session:
        await session.execute(delete(Flashcards).where(Flashcards.id == id))
        await session.commit()


async def sample_cards():
    dataset = {
    # Английский
    ("Apple", "Английский"): ("Яблоко", "Английском", "Английский"),
    ("Dog", "Английский"): ("Собака", "Английском", "Английский"),
    ("Cat", "Английский"): ("Кошка", "Английском", "Английский"),
    ("Book", "Английский"): ("Книга", "Английском", "Английский"),
    ("House", "Английский"): ("Дом", "Английском", "Английский"),
    ("Water", "Английский"): ("Вода", "Английском", "Английский"),
    ("Sun", "Английский"): ("Солнце", "Английском", "Английский"),
    ("Friend", "Английский"): ("Друг", "Английском", "Английский"),
    ("Time", "Английский"): ("Время", "Английском", "Английский"),
    ("Car", "Английский"): ("Машина", "Английском", "Английский"),

    # Японский
    ("りんご", "Японский"): ("Яблоко", "Японском", "Японский"),
    ("いぬ", "Японский"): ("Собака", "Японском", "Японский"),
    ("ねこ", "Японский"): ("Кошка", "Японском", "Японский"),
    ("ほん", "Японский"): ("Книга", "Японском", "Японский"),
    ("いえ", "Японский"): ("Дом", "Японском", "Японский"),
    ("みず", "Японский"): ("Вода", "Японском", "Японский"),
    ("たいよう", "Японский"): ("Солнце", "Японском", "Японский"),
    ("ともだち", "Японский"): ("Друг", "Японском", "Японский"),
    ("じかん", "Японский"): ("Время", "Японском", "Японский"),
    ("くるま", "Японский"): ("Машина", "Японском", "Японский"),

    # Немецкий
    ("Apfel", "Немецкий"): ("Яблоко", "Немецком", "Немецкий"),
    ("Hund", "Немецкий"): ("Собака", "Немецком", "Немецкий"),
    ("Katze", "Немецкий"): ("Кошка", "Немецком", "Немецкий"),
    ("Buch", "Немецкий"): ("Книга", "Немецком", "Немецкий"),
    ("Haus", "Немецкий"): ("Дом", "Немецком", "Немецкий"),
    ("Wasser", "Немецкий"): ("Вода", "Немецком", "Немецкий"),
    ("Sonne", "Немецкий"): ("Солнце", "Немецком", "Немецкий"),
    ("Freund", "Немецкий"): ("Друг", "Немецком", "Немецкий"),
    ("Zeit", "Немецкий"): ("Время", "Немецком", "Немецкий"),
    ("Auto", "Немецкий"): ("Машина", "Немецком", "Немецкий"),

    # Испанский
    ("Manzana", "Испанский"): ("Яблоко", "Испанском", "Испанский"),
    ("Perro", "Испанский"): ("Собака", "Испанском", "Испанский"),
    ("Gato", "Испанский"): ("Кошка", "Испанском", "Испанский"),
    ("Libro", "Испанский"): ("Книга", "Испанском", "Испанский"),
    ("Casa", "Испанский"): ("Дом", "Испанском", "Испанский"),
    ("Agua", "Испанский"): ("Вода", "Испанском", "Испанский"),
    ("Sol", "Испанский"): ("Солнце", "Испанском", "Испанский"),
    ("Amigo", "Испанский"): ("Друг", "Испанском", "Испанский"),
    ("Tiempo", "Испанский"): ("Время", "Испанском", "Испанский"),
    ("Coche", "Испанский"): ("Машина", "Испанском", "Испанский")
}

    async with async_session() as session:
        added_count = 0
        
        for (word, lang), (outword, outlang2, outlang1) in dataset.items():
            # Проверяем, нет ли уже такого слова в БД (как в твоем add_word)
            slovo = await session.scalar(select(Flashcards).where(Flashcards.word == word))
            
            if not slovo:
                # Добавляем точно по твоей структуре полей:
                # word — оригинал, language — язык в им. падеже (outlang1), trword — перевод (outword)
                session.add(Flashcards(
                    word=word, 
                    language=outlang1, 
                    trword=outword
                ))
                added_count += 1
                
        if added_count > 0:
            await session.commit()
            print(f"Успешно добавлено {added_count} новых тестовых карточек!")
        else:
            print("Все карточки из тестового набора уже есть в базе данных.")
