from abc import ABC, abstractmethod
from typing import List

from models.LibraryModels import Book


class LibraryServicesInterface(ABC):

    @abstractmethod
    async def create_book(self, data: dict) -> Book:
        raise NotImplementedError

    @abstractmethod
    async def get_all_books(self) -> List[Book]:
        raise NotImplementedError

    @abstractmethod
    async def delete_book(self, book_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search_books(self, title: str, author: str, year: int) -> List[Book]:
        raise NotImplementedError

    @abstractmethod
    async def patch_book(self, book_id: int, data: dict) -> Book:
        raise NotImplementedError