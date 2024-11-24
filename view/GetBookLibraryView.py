from infrastructure.menus.console_interface import ConsoleInterface, Menu
from services.interfaces.library_service_interface import LibraryServicesInterface


class GetBookLibraryView:
    def __init__(self, library_service: LibraryServicesInterface, menu: Menu, console: ConsoleInterface):
        self.library_service = library_service
        self.menu = menu
        self.console = console

    async def __call__(self):
        try:
            books = await self.library_service.get_all_books()
            if not books:
                self.console.display_message("На данный момент нет доступных книг.")
            else:

                self.console.display_books(books)

        except Exception as e:
            self.console.display_message(f"Неизвестная ошибка: {e}")