from infrastructure.menus.console_interface import Menu, MenuHandler


class InstallLibraryView:
    def __init__(self, menu_handler: MenuHandler, menu: Menu):
        self.menu_handler = menu_handler
        self.display = menu

    async def __call__(self):
        """
        Метод вызова главного консольного меню
        :return:
        """
        while True:
            action_id = self.display.main_menu()
            await self.menu_handler.execute_action(action_id)
