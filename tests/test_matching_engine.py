
import pytest

from src.matching_engine import (
    calculate_skill_match,
    calculate_text_similarity,
    calculate_experience_match,
    calculate_education_match,
)


def test_perfect_skill_match():
    result = calculate_skill_match(
        ["python", "sql", "machine learning"],
        ["python", "sql"],
    )

    assert result["score"] == 100.0
    assert result["missing_skills"] == []


def test_partial_skill_match():
    result = calculate_skill_match(
        ["python", "sql"],
        ["python", "sql", "docker", "aws"],
    )

    assert result["score"] == 50.0
    assert "docker" in result["missing_skills"]


def test_empty_required_skills():
    result = calculate_skill_match(["python"], [])

    assert result["score"] == 0.0


def test_text_similarity():
    score = calculate_text_similarity(
        "Python developer with machine learning experience",
        "Looking for a Python developer with machine learning skills",
    )

    assert 0 <= score <= 100
    assert score > 0


def test_empty_text_similarity():
    assert calculate_text_similarity("", "Python developer") == 0.0


def test_perfect_experience_match():
    assert calculate_experience_match(3, 2) == 100.0


def test_partial_experience_match():
    assert calculate_experience_match(1, 2) == 50.0


def test_missing_experience_requirement():
    assert calculate_experience_match(3, None) == 0.0


def test_negative_experience():
    with pytest.raises(ValueError):
        calculate_experience_match(-1, 2)


def test_education_match():
    score = calculate_education_match(
        ["bca", "mca"],
        ["mca"],
    )

    assert score == 100.0


def test_missing_education_match():
    score = calculate_education_match(
        ["bca"],
        ["mca"],
    )

    assert score == 0.0
