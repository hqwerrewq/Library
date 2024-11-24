from infrastructure.menus.console_interface import delete_book_menu
from services.interfaces.library_service_interface import ILibraryServices


class DeleteBookLibraryView:
    def __init__(self, library_service: ILibraryServices):
        self.library_service = library_service

    async def __call__(self):

        book_id = delete_book_menu()

        await self.library_service.delete_book(book_id)