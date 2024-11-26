import os


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

    def display_books(self, books):
        # Проверка, является ли переданный объект списком книг
        if isinstance(books, list):
            # Если это список, выводим каждую книгу в списке
            for index, book in enumerate(books, start=1):
                self._display_book_details(book, index)
        else:
            # Если это одиночная книга, выводим её детали
            self._display_book_details(books)

    def _display_book_details(self, book, index=None):
        """
        Вспомогательный метод для отображения деталей книги.
        Если индекс передан, он будет отображён в сообщении.
        """
        if index:
            self.display_message(f"Книга #{index}:")

        self.display_message(f"  ID: {book.id}")
        self.display_message(f"  Название: {book.title}")
        self.display_message(f"  Автор: {book.author}")
        self.display_message(f"  Год выпуска: {book.year}")
        status_message = "в наличии" if book.status else "выдана"
        self.display_message(f"  Статус: {status_message}")
        self.display_message("-" * 30)


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

    def create_book_menu(self):

        """Меню для создания книги."""

        self.console.display_message('Меню создания книги.')
        while True:
            try:
                title = self.console.prompt('Введите название новой книги: ').strip()
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

    def search_book_menu(self):

        """Меню для поиска книги по параметрам."""
        self.console.display_message('Меню поиска книги.')
        self.console.display_message('Введите параметры поиска книги, ненужные параметры оставьте пустыми.')
        while True:
            try:
                title = self.console.prompt('Введите название книги: ').strip()

                author = self.console.prompt('Введите автора книги: ').strip()

                year_input = self.console.prompt('Введите год издания книги: ').strip()

                if year_input:
                    year = int(year_input)
                    if year < 0 or year > 2100:
                        raise ValueError('Год издания должен быть реальным (от 0 до 2100).')
                else:
                    year = None

                return {'title': title, 'author': author, 'year': year}

            except ValueError as e:
                self.console.display_message(f"Ошибка ввода: {e}")
                self.console.display_message("Попробуйте ещё раз.\n")

    def patch_book_menu(self) -> dict:
        """
        Меню для изменения статуса книги.
        """
        self.console.display_message('Меню изменения статуса книги.')

        while True:
            try:
                book_id = self.console.prompt('Введите ID книги что бы изменить ее статус (например, "nwpMYCB0"): ').strip()

                if not book_id:
                    raise ValueError('ID книги не может быть пустым.')

                self.console.clear_console()
                self.console.display_message('Выберите статус книги.')
                self.console.display_message('1. В наличии')
                self.console.display_message('2. Выдана')
                status_input = self.console.prompt('Введите номер статуса (1 или 2): ').strip()

                if not status_input.isdigit():
                    raise ValueError('Номер статуса должен быть целым числом.')

                status = int(status_input)

                if status not in {1, 2}:
                    raise ValueError('Пожалуйста, выберите число 1 или 2.')

                # Возвращаем словарь с ID книги и статусом
                return {'book_id': book_id, 'status': status == 1}

            except ValueError as e:
                self.console.display_message(f"Ошибка: {e}")
                self.console.display_message("Попробуйте ещё раз.\n")

    def delete_book_menu(self):
        self.console.display_message('Меню удаления книги.')
        while True:
            try:
                book_id = self.console.prompt('Введите ID книги что бы удалить её. (например, "nwpMYCB0"): ').strip()

                if not book_id:
                    raise ValueError('ID книги не может быть пустым.')

                return book_id

            except ValueError as e:
                self.console.display_message(f"Ошибка: {e}")
                self.console.display_message("Попробуйте ещё раз.\n")

