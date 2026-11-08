
import pytest

from src.education_extractor import extract_education


def test_extract_bachelors():
    result = extract_education(
        "Bachelor of Computer Applications (BCA)"
    )

    assert "bca" in result["qualifications"]
    assert "bca" in result["qualifications_by_level"]["bachelors"]


def test_extract_masters():
    result = extract_education(
        "Master of Computer Applications (MCA)"
    )

    assert "mca" in result["qualifications"]
    assert "mca" in result["qualifications_by_level"]["masters"]


def test_extract_multiple_qualifications():
    result = extract_education(
        "BCA and MCA qualifications"
    )

    assert "bca" in result["qualifications"]
    assert "mca" in result["qualifications"]


def test_extract_phd():
    result = extract_education("PhD in Computer Science")

    assert "phd" in result["qualifications_by_level"]["doctorate"]


def test_empty_text():
    result = extract_education("")

    assert result["qualifications"] == []


def test_invalid_input():
    with pytest.raises(TypeError):
        extract_education(123)


def test_extract_master_of_computer_application():
    result = extract_education(
        "Master of Computer Application (Engg.)"
    )

    assert (
        "master of computer application"
        in result["qualifications"]
    )

    assert (
        "master of computer application"
        in result["qualifications_by_level"]["masters"]
    )