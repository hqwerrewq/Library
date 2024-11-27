import asyncio

from infrastructure.dependency_provider import DependencyProvider
from infrastructure.menus.console_interface import ConsoleInterface, Menu, MenuHandler
from view.CreateBookLibraryView import CreateBookLibraryView
from view.DeleteBookLibraryView import DeleteBookLibraryView
from view.GetBookLibraryView import GetBookLibraryView
from view.PatchBookLibraryView import PatchBookLibraryView
from view.SearchBookLibraryView import SearchBookLibraryView
from view.install.InstallLibraryView import InstallLibraryView


def initialize_library_system():

    console_interface = ConsoleInterface()
    dependency_provider = DependencyProvider()
    menu_handler = MenuHandler(console=console_interface)
    menu = Menu(console=console_interface)

    menu_handler.register_action(
        1,
        CreateBookLibraryView(library_service=dependency_provider.get_library_service(), menu=menu,
                              console=console_interface)
    )

    menu_handler.register_action(
        2,
        GetBookLibraryView(library_service=dependency_provider.get_library_service(), menu=menu, console=console_interface),
    )

    menu_handler.register_action(
        3,
        SearchBookLibraryView(library_service=dependency_provider.get_library_service(), menu=menu, console=console_interface),
    )
    menu_handler.register_action(
        4,
        PatchBookLibraryView(library_service=dependency_provider.get_library_service(), menu=menu, console=console_interface),
    )
    menu_handler.register_action(
        5,
        DeleteBookLibraryView(library_service=dependency_provider.get_library_service(), menu=menu, console=console_interface)
    )
    install_view = InstallLibraryView(menu_handler=menu_handler, menu=menu)

    return install_view


async def main():
    install_view = initialize_library_system()
    await install_view()


if __name__ == '__main__':
    asyncio.run(main())
