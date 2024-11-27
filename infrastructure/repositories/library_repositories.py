from abc import ABC
from typing import List, Optional

from infrastructure.functions.random import random_id_generator
from infrastructure.menus.console_interface import ConsoleInterface
from json_database.json_database import JsonDatabase
from models.LibraryModels import Book
from repositories.interfaces.library_repository_interface import LibraryRepositoriesInterface


class LibraryRepositories(LibraryRepositoriesInterface, ABC):

    def __init__(self, console: ConsoleInterface, json_database: JsonDatabase):
        self.console = console
        self.db = json_database

    async def add_one(self, title: str, author: str, year: int) -> Book:
        """Добавление книги."""
        book_id = next(random_id_generator())
        new_book = Book(id=book_id, title=title, author=author, year=year, status=True)

        try:
            self.db.add_record(new_book.__dict__)
            self.console.display_message("Книга успешно добавлена.")
            return new_book
        except Exception as e:
            self.console.display_message(f"Ошибка при добавлении книги: {e}")
            raise ValueError("Не удалось добавить книгу в базу данных.")

    async def get_all(self) -> List[Book]:
        """Получение всех книг."""
        try:
            records = self.db.get_all_records()
            return [Book(**record) for record in records]
        except Exception as e:
            self.console.display_message(f"Ошибка при получении книг: {e}")
            return []

    async def search(self, title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None) -> List[Book]:
        """Поиск книг."""
        books = await self.get_all()
        return [
            book for book in books
            if (title is None or title.lower() in book.title.lower()) and
               (author is None or author.lower() in book.author.lower()) and
               (year is None or str(year) == str(book.year))
        ]

    async def patch(self, book_id: int, data: dict) -> Optional[Book]:
        """Обновление данных книги."""
        updated_record = self.db.update_record(book_id, data)
        if updated_record:
            self.console.display_message(f"Книга с ID {book_id} обновлена.")
            return Book(**updated_record)
        self.console.display_message(f"Книга с ID {book_id} не найдена.")
        return None

    async def delete(self, book_id: int) -> None:
        """Удаление книги."""
        if self.db.delete_record(book_id):
            self.console.display_message(f"Книга с ID {book_id} удалена.")
        else:
            self.console.display_message(f"Книга с ID {book_id} не найдена.")