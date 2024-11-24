from infrastructure.menus.console_interface import ConsoleInterface, Menu
from services.interfaces.library_service_interface import LibraryServicesInterface


class CreateBookLibraryView:
    def __init__(self, library_service: LibraryServicesInterface, menu: Menu, console: ConsoleInterface):
        self.library_service = library_service
        self.menu = menu
        self.console = console

    async def __call__(self):
        """Метод отображения создания книги"""

        # Очищает консоль для лучшей читаемости
        self.console.clear_console()

        # Меню навигации для создания книги, возвращает данные для создания
        create_data = self.menu.create_book_menu()

        if not create_data:
            self.console.display_message("Ошибка: данные книги некорректны или отсутствуют.")
            return

        # Попытка создать книгу через сервис
        try:
            book = await self.library_service.create_book(data=create_data)

            self.console.display_message(f"Книга успешно добавлена в библиотеку:")
            self.console.display_books(book)

        except Exception as e:
            self.console.display_message(f"Ошибка при создании книги: {e}")
