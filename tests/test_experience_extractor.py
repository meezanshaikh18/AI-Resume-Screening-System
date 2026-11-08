
import pytest

from src.experience_extractor import extract_experience


def test_extract_month_year_range():
    result = extract_experience(
        "Python Developer: January 2023 - December 2024"
    )

    assert len(result["experience_entries"]) == 1
    assert result["experience_entries"][0]["start_date"] == "January 2023"
    assert result["experience_entries"][0]["end_date"] == "December 2024"
    assert result["total_experience_months"] == 23


def test_extract_present_range():
    result = extract_experience(
        "Developer: January 2023 - Present"
    )

    assert len(result["experience_entries"]) == 1
    assert result["experience_entries"][0]["is_current"] is True
    assert result["total_experience_months"] >= 0


def test_overlapping_ranges_not_double_counted():
    result = extract_experience(
        "January 2020 - December 2022\n"
        "January 2021 - December 2023"
    )

    assert result["total_experience_months"] == 47


def test_empty_text():
    result = extract_experience("")

    assert result["experience_entries"] == []
    assert result["total_experience_months"] == 0
    assert result["total_experience_years"] == 0


def test_invalid_input():
    with pytest.raises(TypeError):
        extract_experience(123)


def test_invalid_date_range_ignored():
    result = extract_experience(
        "Developer: December 2024 - January 2023"
    )

    assert result["experience_entries"] == []
    assert result["total_experience_months"] == 0
