import json
import os
import tempfile
from unittest.mock import patch, mock_open
from SRC.json_saver import JSONSaver


def test_json_saver_init():
    """Тест инициализации JSONSaver с дефолтным и кастомным именем файла."""
    saver = JSONSaver()
    assert saver._JSONSaver__filename == "vacancies.json"

    saver_custom = JSONSaver("custom.json")
    assert saver_custom._JSONSaver__filename == "custom.json"


def test_json_saver_add_vacancy():
    """Тест добавления вакансий в файл."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp:
        temp_name = temp.name

    try:
        saver = JSONSaver(temp_name)
        vacancy1 = {'id': '1', 'title': 'Python Developer'}
        vacancy2 = {'id': '2', 'title': 'QA Engineer'}

        saver.add_vacancy(vacancy1)
        saver.add_vacancy(vacancy2)

        # Проверяем, что вакансии записались
        with open(temp_name, encoding='utf-8') as f:
            data = json.load(f)
            assert isinstance(data, list)
            assert len(data) == 2
            assert vacancy1 in data
            assert vacancy2 in data
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def test_json_saver_add_duplicate_vacancy():
    """Тест добавления дублирующей вакансии."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp:
        temp_name = temp.name

    try:
        saver = JSONSaver(temp_name)
        vacancy = {'id': '1', 'title': 'Developer'}

        saver.add_vacancy(vacancy)
        saver.add_vacancy(vacancy)  # Добавляем дубликат

        # Проверяем, что дубликат не добавился
        vacancies = saver.get_vacancies()
        assert len(vacancies) == 1
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def test_json_saver_get_vacancies_empty_file():
    """Тест получения вакансий из несуществующего файла."""
    saver = JSONSaver("non_existent_file.json")
    assert saver.get_vacancies() == []


def test_json_saver_get_vacancies_with_data():
    """Тест получения вакансий из файла с данными."""
    mock_data = '[{"id": "1", "title": "Python Developer", "salary": "100000"}]'

    # Патчим И os.path.exists И open
    with patch('SRC.json_saver.os.path.exists', return_value=True), \
            patch('SRC.json_saver.open', mock_open(read_data=mock_data), create=True):
        saver = JSONSaver("test.json")
        vacancies = saver.get_vacancies()

        assert len(vacancies) == 1
        assert vacancies[0]['id'] == "1"
        assert vacancies[0]['title'] == "Python Developer"
        assert vacancies[0]['salary'] == "100000"


def test_json_saver_get_vacancies_with_criteria():
    """Тест фильтрации вакансий по критериям."""
    mock_data = '''[
        {"id": "1", "title": "Python Developer", "company": "TechCorp"},
        {"id": "2", "title": "Java Developer", "company": "DevCorp"},
        {"id": "3", "title": "Python QA", "company": "TestCorp"}
    ]'''

    # Патчим И os.path.exists И open
    with patch('SRC.json_saver.os.path.exists', return_value=True), \
            patch('SRC.json_saver.open', mock_open(read_data=mock_data), create=True):
        saver = JSONSaver("test.json")

        # Фильтруем по title содержащему "python"
        python_vacancies = saver.get_vacancies({"title": "python"})
        assert len(python_vacancies) == 2

        # Фильтруем по company содержащей "tech"
        tech_vacancies = saver.get_vacancies({"company": "tech"})
        assert len(tech_vacancies) == 1
        assert tech_vacancies[0]['company'] == "TechCorp"


def test_json_saver_get_vacancies_corrupted_json():
    """Тест обработки повреждённого JSON файла."""
    corrupted_data = '{"invalid": json}'

    # Патчим И os.path.exists И open
    with patch('SRC.json_saver.os.path.exists', return_value=True), \
            patch('SRC.json_saver.open', mock_open(read_data=corrupted_data), create=True):
        saver = JSONSaver("test.json")
        vacancies = saver.get_vacancies()
        assert vacancies == []


def test_json_saver_delete_vacancy():
    """Тест удаления вакансии из файла."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp:
        initial_data = [
            {'id': '1', 'title': 'Python Developer'},
            {'id': '2', 'title': 'QA Engineer'},
            {'id': '3', 'title': 'DevOps'}
        ]
        json.dump(initial_data, temp, ensure_ascii=False, indent=2)
        temp_name = temp.name

    try:
        saver = JSONSaver(temp_name)
        vacancy_to_delete = {'id': '2', 'title': 'QA Engineer'}

        saver.delete_vacancy(vacancy_to_delete)

        # Проверяем, что вакансия удалилась
        remaining_vacancies = saver.get_vacancies()
        assert len(remaining_vacancies) == 2
        assert vacancy_to_delete not in remaining_vacancies
        assert {'id': '1', 'title': 'Python Developer'} in remaining_vacancies
        assert {'id': '3', 'title': 'DevOps'} in remaining_vacancies
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def test_json_saver_delete_nonexistent_vacancy():
    """Тест удаления несуществующей вакансии."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp:
        initial_data = [{'id': '1', 'title': 'Developer'}]
        json.dump(initial_data, temp, ensure_ascii=False, indent=2)
        temp_name = temp.name

    try:
        saver = JSONSaver(temp_name)
        nonexistent_vacancy = {'id': '999', 'title': 'Nonexistent'}

        saver.delete_vacancy(nonexistent_vacancy)

        # Проверяем, что исходные данные не изменились
        vacancies = saver.get_vacancies()
        assert len(vacancies) == 1
        assert vacancies[0] == {'id': '1', 'title': 'Developer'}
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def test_json_saver_write_all():
    """Тест вспомогательного метода _write_all."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp:
        temp_name = temp.name

    try:
        saver = JSONSaver(temp_name)
        test_data = [
            {'id': '1', 'title': 'Test Vacancy 1'},
            {'id': '2', 'title': 'Test Vacancy 2'}
        ]

        # Вызываем приватный метод напрямую (он называется _write_all, не __write_all)
        saver._write_all(test_data)

        # Проверяем, что данные записались корректно
        with open(temp_name, encoding='utf-8') as f:
            written_data = json.load(f)
            assert written_data == test_data
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
