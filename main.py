from SRC.hh_api import HeadHunterAPI
from SRC.vacancy import Vacancy
from SRC.json_saver import JSONSaver

def user_interaction():
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    query = input("Введите поисковый запрос: ")

    # Получение вакансий с hh.ru (список dict)
    vacancies_data = hh_api.get_vacancies(query)
    print(f"Получено вакансий: {len(vacancies_data)}")

    # Преобразование в объекты Vacancy
    vacancy_objs = []
    for v in vacancies_data:
        vacancy = Vacancy(
            id=v.get("id", ""),
            title=v.get("name", ""),
            link=v.get("alternate_url", ""),
            company=v.get("employer", {}).get("name", ""),
            area=v.get("area", {}).get("name", ""),
            salary_from=(v["salary"]["from"] if v.get("salary") and v["salary"].get("from") is not None else None),
            salary_to=(v["salary"]["to"] if v.get("salary") and v["salary"].get("to") is not None else None),
            salary_currency=(v["salary"]["currency"] if v.get("salary") and v["salary"].get("currency") else "RUR"),
            description=v.get("description", ""),
            published_at=v.get("published_at", ""),
            snippet_requirement=v.get("snippet", {}).get("requirement", ""),
            snippet_responsibility=v.get("snippet", {}).get("responsibility", ""),
            experience=v.get("experience", {}).get("name", ""),
            employment=v.get("employment", {}).get("name", "")
        )
        vacancy_objs.append(vacancy)

    print(f"Вакансий успешно обработано: {len(vacancy_objs)}")

    # Сохраняем вакансии без дублей
    added = 0
    for v in vacancy_objs:
        existing = [vc["id"] for vc in json_saver.get_vacancies()]
        if v.id not in existing:
            json_saver.add_vacancy(v.to_dict())
            added += 1
    print(f"Сохранено новых вакансий: {added}")

    # Вывод топ-N по зарплате
    n = int(input("Введите количество вакансий для вывода в топ N: "))
    # Отсортировать по средней зарплате (убывание)
    sorted_vacs = sorted([v for v in vacancy_objs if v.get_avg_salary() > 0], reverse=True)
    print(f"\nТОП-{n} вакансий по зарплате:\n" + "-"*40)
    for v in sorted_vacs[:n]:
        print(f"{v.title} — {v.company} — {v.get_avg_salary()} {v.salary_currency} — {v.link}")

    # Фильтрация по ключевому слову
    word = input("\nВведите ключевое слово для фильтрации по описанию/требованиям: ").strip().lower()
    filtered = [
        v for v in vacancy_objs
        if word in (v.description or "").lower() or word in (v.snippet_requirement or "").lower() or word in (v.snippet_responsibility or "").lower()
    ]

    print(f"\nВакансий по фильтру '{word}': {len(filtered)}")
    for v in filtered:
        print(f"{v.title} — {v.company} — {v.link}")
        print(f"  Требования: {v.snippet_requirement}")
        print(f"  Описание: {v.description[:120]}...\n")

    # Возможность удалить вакансию
    to_delete = input("\nХотите удалить вакансию? Введите ID (или Enter для пропуска): ").strip()
    if to_delete:
        all_vacs = json_saver.get_vacancies()
        found = next((v for v in all_vacs if v.get("id") == to_delete), None)
        if found:
            json_saver.delete_vacancy(found)
            print("Вакансия удалена.")
        else:
            print("Вакансия с таким ID не найдена в файле.")

    print("\nРабота завершена. Спасибо!")

if __name__ == "__main__":
    user_interaction()
