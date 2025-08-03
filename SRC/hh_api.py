import requests
from typing import List, Dict, Optional
from SRC.api_base import VacancyAPI


class HeadHunterAPI(VacancyAPI):
    """
    Класс для работы с API hh.ru - получение вакансий по ключевому слову.
    Наследуется от абстрактного VacancyAPI.
    """

    def __init__(self, session=None):
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__session = session if session is not None else requests.Session()
        self.__session.headers.update({
            "User-Agent": "python-requests/2.31.0",
            "Accept": "application/json"
        })

    def __connect(self, params: Dict) -> Optional[requests.Response]:
        """
        Отправка GET-запроса к API hh.ru с указанными параметрами.
        Проверяет код ответа, выбрасывает исключение при ошибках.
        """
        try:
            response = self.__session.get(self.__base_url, params=params, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Ошибка запроса к hh.ru API: {e}")
            return None

    def get_vacancies(self, keyword: str) -> List[Dict]:
        """
        Получение списка вакансий по ключевому слову.
        Параметры запроса:
            - text: поисковая строка (keyword)
            - area: 113 (Россия)
            - per_page: 100 - максимальное количество вакансий на одной странице
        Возвращает список словарей с вакансиями из ключа 'items'.
        """
        vacancies = []
        page = 0
        per_page = 100
        max_pages = 20  # лимит для защиты от слишком долгих запросов

        while page < max_pages:
            params = {
                "text": keyword,
                "area": 113,
                "per_page": per_page,
                "page": page
            }
            response = self.__connect(params)
            if response is None:
                break

            data = response.json()
            items = data.get('items', [])
            vacancies.extend(items)

            # Проверяем, достигли ли последней страницы
            if page >= data.get('pages', 0) - 1:
                break

            page += 1

        return vacancies
