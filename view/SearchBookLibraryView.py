from infrastructure.menus.console_interface import ConsoleInterface, Menu
from services.interfaces.library_service_interface import LibraryServicesInterface


class SearchBookLibraryView:
    def __init__(self, library_service: LibraryServicesInterface, menu: Menu, console: ConsoleInterface):
        self.library_service = library_service
        self.menu = menu
        self.console = console

    async def __call__(self):
        """Метод отображения поиска книг по параметрам"""
        self.console.clear_console()

        search_data = self.menu.search_book_menu()

        try:

            books = await self.library_service.search_books(**search_data)
            if not books:
                self.console.display_message("Книг по заданным параметрам не найдено.")
            else:
                self.console.display_books(books)

        except Exception as e:
            self.console.display_message(f"Ошибка при поиске книги: {e}")
