import json
from pathlib import Path
from typing import List, Optional, Any


class JsonDatabase:
    def __init__(self):
        self.file_path = Path("json_database/data.json")

    def _read_data(self) -> List[dict]:
        """Читает данные из JSON файла."""
        if self.file_path.is_file():
            with self.file_path.open("r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []

    def _write_data(self, data: List[dict]) -> None:
        """Записывает данные в JSON файл."""
        with self.file_path.open("w") as file:
            json.dump(data, file, indent=4)

    def add_record(self, record: dict) -> None:
        """Добавляет запись в JSON файл."""
        data = self._read_data()
        data.append(record)
        self._write_data(data)

    def get_all_records(self) -> List[dict]:
        """Возвращает все записи из JSON файла."""
        return self._read_data()

    def update_record(self, record_id: int, updates: dict) -> Optional[dict]:
        """Обновляет запись по ID."""
        data = self._read_data()
        for record in data:
            if record["id"] == record_id:
                record.update(updates)
                self._write_data(data)
                return record
        return None

    def delete_record(self, record_id: int) -> bool:
        """Удаляет запись по ID."""
        data = self._read_data()
        updated_data = [record for record in data if record.get("id") != record_id]
        if len(data) == len(updated_data):
            return False
        self._write_data(updated_data)
        return True