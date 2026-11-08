
import pytest

from src.skill_extractor import (
    extract_skills,
    extract_skills_by_category,
)


def test_extract_common_skills():
    text = """
    Python developer with experience in Machine Learning,
    Pandas, NumPy and SQL.
    """

    skills = extract_skills(text)

    assert "python" in skills
    assert "machine learning" in skills
    assert "pandas" in skills
    assert "numpy" in skills
    assert "sql" in skills


def test_extract_skills_case_insensitive():
    skills = extract_skills("PYTHON, TENSORFLOW and DOCKER")

    assert "python" in skills
    assert "tensorflow" in skills
    assert "docker" in skills


def test_extract_skills_by_category():
    result = extract_skills_by_category(
        "Python, Machine Learning, AWS and PostgreSQL"
    )

    assert "python" in result["programming_languages"]
    assert "machine learning" in result["machine_learning"]
    assert "aws" in result["tools_and_platforms"]
    assert "postgresql" in result["databases"]


def test_custom_skills():
    skills = extract_skills(
        "Experienced developer with Apache Spark",
        custom_skills=["Apache Spark"],
    )

    assert "apache spark" in skills


def test_empty_text():
    assert extract_skills("") == []


def test_invalid_input():
    with pytest.raises(TypeError):
        extract_skills(123)
        

def test_extract_frontend_and_mobile_skills():
    text = (
        "Angular Ionic TypeScript JavaScript "
        "HTML5 CSS3 SCSS NgRx"
    )

    result = extract_skills(text)

    expected = [
        "angular",
        "css3",
        "html5",
        "ionic",
        "javascript",
        "ngrx",
        "scss",
        "typescript",
    ]

    for skill in expected:
        assert skill in result


def test_extract_api_and_devops_skills():
    text = (
        "REST APIs JWT Authentication Git "
        "Bitbucket Azure DevOps CI/CD"
    )

    result = extract_skills(text)

    expected = [
        "rest apis",
        "jwt authentication",
        "git",
        "bitbucket",
        "azure devops",
        "ci/cd",
    ]

    for skill in expected:
        assert skill in result


def test_extract_mobile_development_skills():
    text = (
        "Push Notifications, Offline Data Storage, "
        "Google Maps"
    )

    result = extract_skills(text)

    assert "push notifications" in result
    assert "offline data storage" in result
    assert "google maps" in result
