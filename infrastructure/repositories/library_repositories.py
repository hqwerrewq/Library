import json
from abc import ABC
from pathlib import Path
from typing import List

from infrastructure.functions.TerminalMenu import ConsoleInterface
from infrastructure.functions.random import random_id_generator
from repositories.interfaces.library_repository_interface import LibraryRepositoriesInterface
from models.LibraryModels import Book


class LibraryRepositories(LibraryRepositoriesInterface, ABC):

    def __init__(self, console: ConsoleInterface):
        self.console = console
        self.file_path = Path("json_database/data.json")

    async def add_one(self, title: str, author: str, year: str) -> Book:
        """
        Добавление книги в JSON файл (Базу данных).
        :param title: Название книги
        :param author: Автор книги
        :param year: Год издания книги
        :return: Объект книги
        """
        # Генерация уникального ID для книги
        gen = random_id_generator()
        book_id = next(gen)

        new_book = Book(
            id=book_id,
            title=title,
            author=author,
            year=year,
            status=True
        )

        try:
            if self.file_path.is_file():
                with self.file_path.open("r") as file:
                    try:
                        existing_data = json.load(file)
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []

            # Добавляем книгу в список
            if isinstance(existing_data, list):
                existing_data.append(new_book.__dict__)
            else:
                existing_data = [existing_data, new_book.__dict__]

            # Сохраняем в файл
            with self.file_path.open("w") as file:
                json.dump(existing_data, file, indent=4)

            self.console.display_message(f"Данные успешно сохранены в {self.file_path}")

            return new_book
        except Exception as e:

            self.console.display_message(f"Ошибка при сохранении данных: {e}")

            raise ValueError("Не удалось сохранить книгу в базу данных.")

    async def get_all(self) -> List[Book]:
        """ Получение всех книг из файла и преобразование в объекты Book """
        try:
            if self.file_path.is_file():
                with self.file_path.open("r") as file:
                    try:
                        data = json.load(file)
                        # Преобразуем данные в объекты Book
                        return [Book(**book) for book in data]
                    except json.JSONDecodeError:

                        self.console.display_message("Ошибка чтения JSON, файл поврежден.")

                        return []
            else:
                self.console.display_message("Файл не найден.")
                return []
        except Exception as e:
            # Логирование ошибки (например, файл не доступен)
            self.console.display_message(f"Ошибка при загрузке данных: {e}")
            return []

    async def search(self, title: str = None, author: str = None, year: int = None) -> List[Book]:
        """Поиск книг по параметрам."""
        try:
            # Загружаем данные из файла
            if not self.file_path.is_file():
                self.console.display_message("Файл с книгами не найден.")
                return []

            with self.file_path.open("r") as file:
                try:
                    books_data = json.load(file)
                except json.JSONDecodeError:
                    self.console.display_message("Ошибка чтения JSON, файл поврежден.")
                    return []

            # Преобразуем данные в объекты Book
            books = [Book(**book) for book in books_data]

            # Фильтруем книги по параметрам
            filtered_books = [
                book for book in books
                if (title is None or title.lower() in book.title.lower()) and
                   (author is None or author.lower() in book.author.lower()) and
                   (year is None or str(year) == str(book.year))
            ]

            return filtered_books
        except Exception as e:
            # Логирование или обработка ошибок
            self.console.display_message(f"Ошибка при поиске книг: {e}")
            return []

    async def patch(self, book_id: int, data: dict) -> Book:
        """
        Обновление данных книги в JSON-файле.
        :param book_id: Идентификатор книги для обновления.
        :param data: Словарь с новыми данными для книги.
        :return: Обновленный объект Book.
        """
        try:
            if not self.file_path.is_file():
                raise FileNotFoundError("Файл с книгами не найден.")

            with self.file_path.open("r") as file:
                try:
                    books_data = json.load(file)
                except json.JSONDecodeError:
                    raise ValueError("Ошибка чтения JSON, файл поврежден.")

            # Ищем книгу с указанным ID
            for book in books_data:
                if book["id"] == book_id:
                    # Обновляем только те поля, которые переданы в `data`
                    for key, value in data.items():
                        if key in book:
                            book[key] = value
                    # Перезаписываем файл
                    with self.file_path.open("w") as file:
                        json.dump(books_data, file, indent=4)
                    return Book(**book)

            raise ValueError(f"Книга с ID {book_id} не найдена.")

        except Exception as e:
            # Логируем или обрабатываем ошибку
            print(f"Ошибка при обновлении книги: {e}")
            raise

    async def delete(self, book_id: int) -> None:

        if self.file_path.is_file():
            with self.file_path.open("r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    self.console.display_message("Ошибка чтения JSON. Файл поврежден или пустой.")
                    data = []

            updated_data = [item for item in data if item.get("id") != book_id]


            if len(data) == len(updated_data):
                self.console.display_message(f"Объект с ID {book_id} не найден.")
            else:

                with self.file_path.open("w") as file:
                    json.dump(updated_data, file, indent=4)
                self.console.display_message(f"Объект с ID {book_id} успешно удален.")
        else:
            self.console.display_message("Файл не найден.")