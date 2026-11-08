
import pytest

from src.job_description_parser import (
    extract_experience_requirement,
    extract_required_and_preferred_skills,
    parse_job_description,
)


SAMPLE_JOB = """
Job Title: Junior Machine Learning Engineer

Required Skills:
- Python
- Machine Learning
- SQL
- Scikit-learn

Preferred Skills:
- TensorFlow
- Docker
- AWS

Experience:
Minimum of 2 years of experience.

Education:
Bachelor of Computer Science.
"""


def test_extract_job_title():
    result = parse_job_description(SAMPLE_JOB)

    assert result["job_title"] == "Junior Machine Learning Engineer"


def test_extract_required_skills():
    result = parse_job_description(SAMPLE_JOB)

    required = result["skills"]["required_skills"]

    assert "python" in required
    assert "machine learning" in required
    assert "sql" in required


def test_extract_preferred_skills():
    result = parse_job_description(SAMPLE_JOB)

    preferred = result["skills"]["preferred_skills"]

    assert "tensorflow" in preferred
    assert "docker" in preferred
    assert "aws" in preferred


def test_extract_experience_requirement():
    result = parse_job_description(SAMPLE_JOB)

    assert result["minimum_experience_years"] == 2.0


def test_extract_experience_variations():
    assert extract_experience_requirement(
        "3+ years of experience required"
    ) == 3.0

    assert extract_experience_requirement(
        "At least 5 years of experience"
    ) == 5.0


def test_empty_job_description():
    with pytest.raises(ValueError):
        parse_job_description("")


def test_invalid_input():
    with pytest.raises(TypeError):
        parse_job_description(123)


def test_general_skills():
    result = parse_job_description(
        "Job Title: Python Developer\n"
        "We need experience with Pandas and NumPy."
    )

    assert "pandas" in result["skills"]["all_skills"]
    assert "numpy" in result["skills"]["all_skills"]
    

def test_inline_required_skills():
    text = "Required Skills: Python, SQL, Machine Learning"

    result = extract_required_and_preferred_skills(text)

    assert result["required_skills"] == [
        "machine learning",
        "python",
        "sql",
    ]


def test_parse_job_description_preserves_raw_text():
    text = (
        "Job Title: Python Developer\n"
        "Required Skills: Python, SQL\n"
        "Minimum 2 years of experience"
    )

    result = parse_job_description(text)

    assert result["raw_text"] == text
