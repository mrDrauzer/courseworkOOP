from SRC.vacancy import Vacancy
import pytest

def test_vacancy_initialization():
    v = Vacancy("1", "Разработчик", "url", "Компания", "Москва", 100000, 120000, "RUR", "Описание")
    assert v.id == "1"
    assert v.title == "Разработчик"
    assert v.link == "url"
    assert v.company == "Компания"
    assert v.area == "Москва"
    assert v.salary_from == 100000
    assert v.salary_to == 120000
    assert v.description == "Описание"

def test_vacancy_avg_salary():
    v_full = Vacancy("1", "Dev", "link", "Comp", "Area", 80000, 100000)
    v_from = Vacancy("2", "Dev", "link", "Comp", "Area", 90000, None)
    v_to = Vacancy("3", "Dev", "link", "Comp", "Area", None, 110000)
    v_none = Vacancy("4", "Dev", "link", "Comp", "Area", None, None)

    assert v_full.get_avg_salary() == 90000
    assert v_from.get_avg_salary() == 90000
    assert v_to.get_avg_salary() == 110000
    assert v_none.get_avg_salary() == 0

def test_vacancy_comparison():
    v1 = Vacancy("1", "Dev", "link", "Comp", "Area", 50000)
    v2 = Vacancy("2", "Dev", "link", "Comp", "Area", 60000)
    v3 = Vacancy("3", "Dev", "link", "Comp", "Area", 50000)
    assert v1 < v2
    assert v2 > v1
    assert v1 == v3
    assert v2 != v1

def test_vacancy_to_from_dict():
    vac = Vacancy("1", "Dev", "link", "Comp", "Area", 80000, 100000)
    vac_dict = vac.to_dict()
    vac_copy = Vacancy.from_dict(vac_dict)
    assert vac_copy.title == vac.title
    assert vac_copy.salary_from == vac.salary_from
    assert vac_copy.salary_to == vac.salary_to
    assert vac_copy.to_dict() == vac_dict
