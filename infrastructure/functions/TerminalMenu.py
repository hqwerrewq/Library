import os
import subprocess

class ConsoleInterface:
    @staticmethod
    def clear_console():
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Linux/Mac
            if 'TERM' not in os.environ:
                os.environ['TERM'] = 'xterm'
            os.system('clear')

    @staticmethod
    def prompt(message: str) -> str:
        """Отображает сообщение и получает ввод пользователя."""
        return input(message)

    @staticmethod
    def display_message(message: str):
        """Выводит сообщение в консоль."""
        print(message)


class MenuHandler:
    """Класс для управления меню."""
    def __init__(self, console: ConsoleInterface):
        self.console = console
        self.actions = {}

    def register_action(self, action_id, action):
        self.actions[action_id] = action

    async def execute_action(self, action_id):
        action = self.actions.get(action_id)
        if action:
            await action()
        else:
            self.console.display_message("Invalid menu option")


class Menu:
    """Меню для выбора действий."""
    def __init__(self, console: ConsoleInterface):
        self.console = console
        self.menu_options = {
            1: "Добавление книги",
            2: "Отображение всех книг",
            3: "Поиск книги",
            4: "Изменение статуса книги",
            5: "Удаление книги"
        }

    def main_menu(self):
        """Отображает меню с опциями и получает ввод пользователя."""
        while True:
            self.console.clear_console()
            self.console.display_message("Главное меню:")
            for key, value in self.menu_options.items():
                self.console.display_message(f"{key}. {value}")

            try:
                event = int(self.console.prompt("Введите номер пункта: ").strip())
                if 1 <= event <= len(self.menu_options):
                    return event
                else:
                    self.console.display_message('Пожалуйста, выберите число от 1 до 5.')
            except ValueError:
                self.console.display_message('Ошибка ввода! Введите целое число от 1 до 5.')

    def create_book_menu(self) -> dict:
        """Меню для создания книги."""
        self.console.display_message('Для создания новой книги следуйте пунктам.')
        while True:
            try:
                title = self.console.prompt('Введите название книги: ').strip()
                if not title:
                    raise ValueError('Название книги не может быть пустым.')

                author = self.console.prompt('Введите автора книги: ').strip()
                if not author:
                    raise ValueError('Имя автора не может быть пустым.')

                year_input = self.console.prompt('Введите год издания книги: ').strip()
                if not year_input.isdigit():
                    raise ValueError('Год издания должен быть целым числом.')
                year = int(year_input)
                if year < 0 or year > 2100:
                    raise ValueError('Год издания должен быть реальным (от 0 до 2100).')

                return {'title': title, 'author': author, 'year': year}

            except ValueError as e:
                self.console.display_message(f"Ошибка ввода: {e}")
                self.console.display_message("Попробуйте ещё раз.\n")


# def get_menu():
#     while True:
#         print('1. Добавление книги')
#         print('2. Отображение всех книг')
#         print('3. Поиск книги')
#         print('4. Изменение статуса книги')
#         print('5. Удаление книги')
#         try:
#             event = int(input('Введите номер пункта: '))
#             if 1 <= event <= 5:
#                 return event
#             else:
#                 print('Пожалуйста, выберите число от 1 до 5.')
#         except ValueError:
#             clear_console()
#             print('Ошибка ввода! Введите целое число от 1 до 5.')
#
#
# def get_create_book_menu() -> dict:
#     print('Для создания новой книги следуйте пунктам.')
#     while True:
#         try:
#             title = input('Введите название книги: ').strip()
#             if not title:
#                 raise ValueError('Название книги не может быть пустым.')
#
#             author = input('Введите автора книги: ').strip()
#             if not author:
#                 raise ValueError('Имя автора не может быть пустым.')
#
#             year_input = input('Введите год издания книги: ').strip()
#             if not year_input.isdigit():
#                 raise ValueError('Год издания должен быть целым числом.')
#             year = int(year_input)
#             if year < 0 or year > 2100:
#                 raise ValueError('Год издания должен быть реальным (от 0 до 2100).')
#
#             return {'title': title, 'author': author, 'year': year}
#
#         except ValueError as e:
#             print(f"Ошибка ввода: {e}")
#
#         print("Попробуйте ещё раз.\n")
#
#
# def delete_book_menu():
#     print('Для удаления книги следуйте пунктам')
#     while True:
#         try:
#             book_id = input('Введите айди книги: ').strip()
#             if not book_id:
#                 raise ValueError('Айди книги не может быть пустым.')
#
#             return book_id
#
#         except ValueError as e:
#             print(f"Ошибка ввода: {e}")
#
#         print("Попробуйте ещё раз.\n")
#
#
# def clear_console():
#     if os.name == 'nt':  # Windows
#         os.system('cls')
#     else:  # Linux/Mac
#         # Убедимся, что переменная TERM установлена
#         if 'TERM' not in os.environ:
#             os.environ['TERM'] = 'xterm'
#         os.system('clear')