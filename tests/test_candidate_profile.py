
from pathlib import Path

from src.resume_parser import parse_resume


PDF_PATH = Path("data/sample_data/sample_resume.pdf")


def test_complete_candidate_profile():
    profile = parse_resume(PDF_PATH)

    assert profile["file_name"] == "sample_resume.pdf"

    assert "python" in profile["skills"]
    assert "machine learning" in profile["skills"]

    assert "programming_languages" in profile["skills_by_category"]

    assert "experience" in profile
    assert "education" in profile

    assert profile["experience"]["total_experience_months"] > 0

    assert isinstance(profile["education"]["qualifications"], list)


def test_candidate_profile_contains_raw_text():
    profile = parse_resume(PDF_PATH)

    assert "ALEX JOHNSON" in profile["raw_text"]


def test_candidate_profile_contains_processed_text():
    profile = parse_resume(PDF_PATH)

    assert "python" in profile["processed_text"]
