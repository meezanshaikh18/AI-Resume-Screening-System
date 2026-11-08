
from pathlib import Path

import pytest

from src.resume_parser import parse_resume


PDF_PATH = Path("data/sample_data/sample_resume.pdf")
DOCX_PATH = Path("data/sample_data/sample_resume.docx")


def test_parse_pdf_resume():
    result = parse_resume(PDF_PATH)

    assert result["file_name"] == "sample_resume.pdf"
    assert result["file_type"] == ".pdf"
    assert "python" in result["skills"]
    assert "machine learning" in result["skills"]
    assert result["raw_text"]
    assert result["cleaned_text"]
    assert result["processed_text"]


def test_parse_docx_resume():
    result = parse_resume(DOCX_PATH)

    assert result["file_name"] == "sample_resume.docx"
    assert "python" in result["skills"]
    assert "sql" in result["skills"]


def test_parse_missing_resume():
    with pytest.raises(FileNotFoundError):
        parse_resume("data/sample_data/missing.pdf")


def test_parse_unsupported_resume(tmp_path):
    file_path = tmp_path / "resume.txt"
    file_path.write_text("Python developer")

    with pytest.raises(ValueError, match="Unsupported file format"):
        parse_resume(file_path)


def test_categorized_skills():
    result = parse_resume(PDF_PATH)

    categories = result["skills_by_category"]

    assert "python" in categories["programming_languages"]
    assert "machine learning" in categories["machine_learning"]
    assert "sql" in categories["programming_languages"]
