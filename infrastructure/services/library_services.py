from abc import ABC
from typing import List

from infrastructure.functions.TerminalMenu import ConsoleInterface
from repositories.interfaces.library_repository_interface import LibraryRepositoriesInterface
from services.interfaces.library_service_interface import LibraryServicesInterface
from models.LibraryModels import Book


class LibraryServices(LibraryServicesInterface, ABC):
    def __init__(self, library_repository: LibraryRepositoriesInterface, console: ConsoleInterface):
        self.library_repository = library_repository
        self.console = console

    async def create_book(self, data: dict) -> Book:
        """
        Создание книги
        :param data: Данные для создания книги
        :return: Созданная книга
        """
        try:
            # Делаем вызов репозитория для добавления книги
            created_book = await self.library_repository.add_one(
                title=data['title'],
                author=data['author'],
                year=data['year'],
            )
            return created_book
        except Exception as e:
            self.console.display_message(f"Ошибка при создании книги: {e}")
            raise e

    async def get_all_books(self) -> List[Book]:
        """
        Получение списка всех книг
        """
        try:
            books = await self.library_repository.get_all()

            if not books:
                return []  # Возвращаем пустой список, если книг нет
            return books  # Возвращаем книги, если они есть

        except Exception as e:
            # Логирование или обработка ошибок
            self.console.display_message(f"Ошибка при получении книг: {e}")
            return []  # Возвращаем пустой список в случае ошибки

    async def search_books(self, title: str = None, author: str = None, year: int = None) -> List[Book]:
        """
        Поиск книг по параметрам через репозиторий.
        :param title: Название книги (необязательно).
        :param author: Автор книги (необязательно).
        :param year: Год издания книги (необязательно).
        :return: Список найденных книг.
        """
        try:
            # Вызываем метод репозитория для поиска книг
            books = await self.library_repository.search(title=title, author=author, year=year)

            if not books:
                # Если книги не найдены, логируем сообщение
                print("Книги соответствующие параметрам поиска, не найдены.")

            return books
        except Exception as e:
            # Обработка ошибок уровня репозитория или других исключений
            print(f"Ошибка при выполнении поиска книг: {e}")
            return []

    async def patch_book(self, book_id: int, data: dict) -> Book:
        """
        Обновление данных книги.
        :param book_id: Идентификатор книги для обновления.
        :param data: Словарь с новыми данными для книги.
        :return: Обновленный объект Book.
        """
        # Проверяем входные данные (можно также использовать pydantic-схему для валидации)
        if not data:
            raise ValueError("Переданы пустые данные для обновления.")

        # Пробуем обновить книгу через репозиторий
        try:
            updated_book = await self.library_repository.patch(book_id, data)
            return updated_book

        except ValueError as e:
            raise ValueError(f"Ошибка в данных или книга с ID {book_id} не найдена: {e}")
        except Exception as e:
            # Логирование можно заменить на библиотеку logging
            print(f"Неожиданная ошибка при обновлении книги: {e}")

    async def delete_book(self, book_id: int) -> None:
        await self.library_repository.delete(book_id)