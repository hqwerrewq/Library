from infrastructure.menus.console_interface import Menu, ConsoleInterface
from services.interfaces.library_service_interface import LibraryServicesInterface


class DeleteBookLibraryView:
    def __init__(self, library_service: LibraryServicesInterface, menu: Menu, console: ConsoleInterface):
        self.library_service = library_service
        self.menu = menu
        self.console = console

    async def __call__(self):
        self.console.clear_console()
        book_id = self.menu.delete_book_menu()

        await self.library_service.delete_book(book_id)