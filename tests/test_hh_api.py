from unittest.mock import Mock, patch
import requests
from SRC.hh_api import HeadHunterAPI


def test_hh_api_init():
    """Тест инициализации HeadHunterAPI."""
    api = HeadHunterAPI()
    assert api._HeadHunterAPI__base_url == "https://api.hh.ru/vacancies"
    assert isinstance(api._HeadHunterAPI__session, requests.Session)


def test_hh_api_init_with_custom_session():
    """Тест инициализации с кастомной сессией."""
    mock_session = Mock()
    api = HeadHunterAPI(session=mock_session)
    assert api._HeadHunterAPI__session == mock_session


def test_hh_api_get_vacancies():
    """Тест получения вакансий от API."""
    mock_response = Mock()
    mock_response.json.return_value = {
        'items': [
            {'id': '1', 'name': 'Python Developer'},
            {'id': '2', 'name': 'Java Developer'}
        ],
        'pages': 1
    }
    mock_response.status_code = 200

    mock_session = Mock()
    mock_session.get.return_value = mock_response

    api = HeadHunterAPI(session=mock_session)
    vacancies = api.get_vacancies("python")

    assert len(vacancies) == 2
    assert vacancies[0]['id'] == '1'
    assert vacancies[1]['name'] == 'Java Developer'


def test_hh_api_get_vacancies_request_error():
    """Тест обработки ошибки запроса."""
    mock_session = Mock()
    mock_session.get.side_effect = requests.RequestException("Connection error")

    api = HeadHunterAPI(session=mock_session)
    vacancies = api.get_vacancies("python")

    assert vacancies == []
