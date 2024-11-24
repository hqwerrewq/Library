from abc import ABC, abstractmethod
from typing import List

from models.LibraryModels import Book


class LibraryRepositoriesInterface(ABC):


    @abstractmethod
    async def get_all(self) -> List[Book]:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, title: str, author: str, year: str) -> Book:
        raise NotImplementedError


    @abstractmethod
    async def delete(self, book_id: int)-> None:
        raise NotImplementedError

    @abstractmethod
    async def search(self, title: str, author: str, year: int) -> List[Book]:
        raise NotImplementedError

    @abstractmethod
    async def patch(self, book_id: int, data: dict) -> Book:
        raise NotImplementedError