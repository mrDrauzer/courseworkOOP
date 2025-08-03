from abc import ABC, abstractmethod
from typing import List, Dict

class VacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict]:
        pass
