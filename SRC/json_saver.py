import json
import os
from typing import List, Dict, Optional
from SRC.file_connector import FileSaver


class JSONSaver(FileSaver):
    """
    Класс для хранения вакансий в JSON-файле.
    """

    def __init__(self, filename: str = "vacancies.json"):
        self.__filename = filename

    def add_vacancy(self, vacancy: Dict) -> None:
        """Добавляет вакансию в файл, если дубликата нет."""
        vacancies = self.get_vacancies()
        if vacancy not in vacancies:
            vacancies.append(vacancy)
            self._write_all(vacancies)
        else:
            print("Вакансия уже есть в файле.")

    def get_vacancies(self, criteria: Optional[Dict] = None) -> List[Dict]:
        """Возвращает список вакансий, опционально фильтрует по критериям."""
        if not os.path.exists(self.__filename):
            return []

        with open(self.__filename, encoding="utf-8") as f:
            try:
                vacancies = json.load(f)
            except Exception:
                vacancies = []

        if criteria:
            # Пример простой фильтрации по ключу и значению
            key, value = list(criteria.items())[0]
            return [
                v
                for v in vacancies
                if value.lower() in str(v.get(key, "")).lower()
            ]
        return vacancies

    def delete_vacancy(self, vacancy: Dict) -> None:
        """Удаляет конкретную вакансию из файла."""
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v != vacancy]
        self._write_all(vacancies)

    def _write_all(self, vacancies: List[Dict]) -> None:
        """Вспомогательный метод для записи всех вакансий в JSON."""
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)
