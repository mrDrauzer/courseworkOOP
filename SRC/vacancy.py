from typing import Optional, Dict


class Vacancy:
    """
    Класс вакансии с поддержкой сравнения, валидацией и удобством для хранения.
    """

    __slots__ = (
        "id",
        "title",
        "link",
        "company",
        "area",
        "salary_from",
        "salary_to",
        "salary_currency",
        "description",
        "published_at",
        "snippet_requirement",
        "snippet_responsibility",
        "experience",
        "employment",
    )

    def __init__(
        self,
        id: str,
        title: str,
        link: str,
        company: str,
        area: str,
        salary_from: Optional[int] = None,
        salary_to: Optional[int] = None,
        salary_currency: str = "RUR",
        description: Optional[str] = "",
        published_at: Optional[str] = "",
        snippet_requirement: Optional[str] = "",
        snippet_responsibility: Optional[str] = "",
        experience: Optional[str] = "",
        employment: Optional[str] = "",
    ):
        self.id = id
        self.title = title
        self.link = link
        self.company = company
        self.area = area
        self.salary_from = self._validate_salary(salary_from)
        self.salary_to = self._validate_salary(salary_to)
        self.salary_currency = salary_currency or "RUR"
        self.description = description or ""
        self.published_at = published_at or ""
        self.snippet_requirement = snippet_requirement or ""
        self.snippet_responsibility = snippet_responsibility or ""
        self.experience = experience or ""
        self.employment = employment or ""

    def _validate_salary(self, value):
        if value is None or not isinstance(value, (int, float)):
            return 0
        return int(value)

    def get_avg_salary(self) -> int:
        """Возвращает среднюю зарплату по вакансии,
         если две границы, иначе одну."""
        if self.salary_from and self.salary_to:
            return (self.salary_from + self.salary_to) // 2
        return self.salary_from or self.salary_to or 0

    # Сравнения по средней зарплате
    def __eq__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_avg_salary() == other.get_avg_salary()

    def __lt__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_avg_salary() < other.get_avg_salary()

    def __gt__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_avg_salary() > other.get_avg_salary()

    def __repr__(self):
        salary = self.get_avg_salary()
        return (
            f"Vacancy('{self.title}', компания: {self.company}, регион: {self.area}, "
            f"зарплата: {salary} {self.salary_currency}, ссылка: {self.link})"
        )

    def to_dict(self) -> dict:
        """Преобразует Vacancy в словарь (для json хранилища)."""
        return {
            "id": self.id,
            "title": self.title,
            "link": self.link,
            "company": self.company,
            "area": self.area,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "salary_currency": self.salary_currency,
            "description": self.description,
            "published_at": self.published_at,
            "snippet_requirement": self.snippet_requirement,
            "snippet_responsibility": self.snippet_responsibility,
            "experience": self.experience,
            "employment": self.employment,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Vacancy":
        """Создаёт Vacancy из dict (например, из JSON)."""
        return cls(
            id=data.get("id", ""),
            title=data.get("title", data.get("name", "")),
            link=data.get("link", data.get("url", "")),
            company=data.get("company", ""),
            area=data.get("area", ""),
            salary_from=data.get("salary_from", None),
            salary_to=data.get("salary_to", None),
            salary_currency=data.get("salary_currency", "RUR"),
            description=data.get("description", ""),
            published_at=data.get("published_at", ""),
            snippet_requirement=data.get("snippet_requirement", ""),
            snippet_responsibility=data.get("snippet_responsibility", ""),
            experience=data.get("experience", ""),
            employment=data.get("employment", ""),
        )
