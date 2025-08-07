from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class FileSaver(ABC):
    """
    Абстрактный базовый класс для работы с файловым хранилищем вакансий.
    Определяет методы добавления, получения и удаления вакансий.
    Конкретные реализации (JSON, CSV, БД и т.д.)
    должны наследовать этот класс и реализовывать методы.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Dict) -> None:
        """
        Добавить вакансию в хранилище.
        :param vacancy: Словарь с данными вакансии.
        """
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Optional[Dict] = None) -> List[Dict]:
        """
        Получить список вакансий из хранилища,
        с опциональной фильтрацией по критериям.
        :param criteria: Словарь с критериями фильтрации
         (например, ключевые слова, диапазон зарплат и т.п.)
        :return: Список словарей с вакансиями.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Dict) -> None:
        """
        Удалить вакансию из хранилища.
        :param vacancy: Словарь с данными вакансии, которую нужно удалить.
        """
        pass
