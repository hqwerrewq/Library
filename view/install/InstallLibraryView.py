from infrastructure.menus.console_interface import Menu, MenuHandler


class InstallLibraryView:
    def __init__(self, menu_handler: MenuHandler, menu: Menu):
        self.menu_handler = menu_handler
        self.display = menu

    async def __call__(self):
        while True:
            action_id = self.display.main_menu()
            await self.menu_handler.execute_action(action_id)

        # create_book_library_view = CreateBookLibraryView(
        #     library_service=LibraryServices(
        #         library_repository=LibraryRepositories()
        #     )
        # )
        #
        # get_book_library_view = GetBookLibraryView(
        #     library_service=LibraryServices(
        #         library_repository=LibraryRepositories()
        #     )
        # )
        #
        #
        # delete_book_library_view = DeleteBookLibraryView(
        #     library_service=LibraryServices(
        #         library_repository=LibraryRepositories()
        #     )
        # )
        #
        # while True:
        #     menu = get_menu()
        #
        #     if menu == 1:
        #         await create_book_library_view.__call__()
        #
        #     if menu == 2:
        #         await get_book_library_view.__call__()
        #
        #     if menu == 5:
        #         await delete_book_library_view.__call__()
