from infrastructure.menus.console_interface import Menu, ConsoleInterface
from services.interfaces.library_service_interface import LibraryServicesInterface


class PatchBookLibraryView:
    def __init__(self, library_service: LibraryServicesInterface, menu: Menu, console: ConsoleInterface):
        self.library_service = library_service
        self.menu = menu
        self.console = console


    async def __call__(self):
        """Метод отображения обновления данных книги, в данном случае, только статуса"""
        self.console.clear_console()

        patch_data = self.menu.patch_book_menu()

        try:
            book = await self.library_service.patch_book(book_id=patch_data['book_id'], data=patch_data)

            self.console.display_message(f"Статус книги успешно изменен:")
            self.console.display_books(book)

        except Exception as e:
            self.console.display_message(f"Ошибка при изменение книги: {e}")

