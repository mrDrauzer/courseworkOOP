from SRC.helpers import filter_vacancies_by_keyword, sort_vacancies_by_salary, get_top_vacancies

def test_filter_vacancies_by_keyword():
    vacancies = [
        {'description': 'Нужен python-разработчик'},
        {'description': 'Java Developer'},
        {'description': 'QA Engineer', 'snippet_requirement': 'Знание python будет плюсом'},
        {'description': 'Продажи'}
    ]
    filtered = filter_vacancies_by_keyword(vacancies, ['python'])
    assert len(filtered) == 2
    assert filtered[0]['description'] == 'Нужен python-разработчик'
    assert filtered[1]['description'] == 'QA Engineer'

def test_sort_vacancies_by_salary():
    vacancies = [
        {'salary_from': 80000},
        {'salary_from': 60000},
        {'salary_from': 100000}
    ]
    sorted_vacs = sort_vacancies_by_salary(vacancies)
    assert sorted_vacs[0]['salary_from'] == 100000
    assert sorted_vacs[2]['salary_from'] == 60000

def test_get_top_vacancies():
    vacancies = [{'salary_from': 1}, {'salary_from': 2}, {'salary_from': 3}]
    top = get_top_vacancies(vacancies, 2)
    assert len(top) == 2
