from infrastructure.functions.TerminalMenu import ConsoleInterface
from infrastructure.repositories.library_repositories import LibraryRepositories
from infrastructure.services.library_services import LibraryServices
from repositories.interfaces.library_repository_interface import LibraryRepositoriesInterface
from services.interfaces.library_service_interface import LibraryServicesInterface


class DependencyProvider:
    def __init__(
        self,
        library_service: LibraryServicesInterface = None,
        library_repository: LibraryRepositoriesInterface = None,
    ):
        self._library_repository = (
            library_repository or LibraryRepositories(console=ConsoleInterface())
        )
        self._library_service = (
            library_service or LibraryServices(library_repository=self._library_repository, console=ConsoleInterface())
        )

    def get_library_service(self) -> LibraryServicesInterface:
        """Получение экземпляра сервиса библиотеки."""
        return self._library_service

    def get_library_repository(self) -> LibraryRepositoriesInterface:
        """Получение экземпляра репозитория библиотеки."""
        return self._library_repository

    def set_library_service(self, library_service: LibraryServicesInterface):
        """Метод для установки кастомного сервиса библиотеки."""
        self._library_service = library_service

    def set_library_repository(self, library_repository: LibraryRepositoriesInterface):
        """Метод для установки кастомного репозитория библиотеки."""
        self._library_repository = library_repository