from typing import List, Dict, Callable

def filter_vacancies_by_keyword(vacancies: List[Dict], keywords: List[str]) -> List[Dict]:
    """
    Фильтрация вакансий по наличию ключевых слов в описании или требованиях.
    """
    keywords = [kw.lower() for kw in keywords]
    def matches(vacancy: Dict) -> bool:
        text = (
            str(vacancy.get('description', '')) +
            str(vacancy.get('snippet_requirement', '')) +
            str(vacancy.get('snippet_responsibility', ''))
        ).lower()
        return any(kw in text for kw in keywords)
    return [v for v in vacancies if matches(v)]

def sort_vacancies_by_salary(vacancies: List[Dict], descending: bool = True) -> List[Dict]:
    """
    Сортировка вакансий по зарплате (по убыванию по умолчанию).
    """
    return sorted(
        vacancies,
        key=lambda v: v.get('salary_from') or v.get('salary_to') or 0,
        reverse=descending
    )

def get_top_vacancies(vacancies: List[Dict], n: int) -> List[Dict]:
    """
    Возвращает топ n вакансий из переданного списка.
    """
    return vacancies[:n]

def filter_by_salary_range(
    vacancies: List[Dict],
    min_salary: int = 0,
    max_salary: int = 1_000_000
) -> List[Dict]:
    """
    Фильтр по диапазону зарплаты (берется salary_from либо salary_to по возможности).
    """
    result = []
    for v in vacancies:
        sf = v.get("salary_from") or 0
        st = v.get("salary_to") or 0
        avg_salary = (sf + st) // 2 if sf and st else (sf or st)
        if min_salary <= avg_salary <= max_salary:
            result.append(v)
    return result
