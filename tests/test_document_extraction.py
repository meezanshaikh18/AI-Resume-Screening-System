
from pathlib import Path

from src.document_processor import extract_text


def test_pdf_extraction():
    path = Path("data/sample_data/sample_resume.pdf")
    text = extract_text(path)

    assert "ALEX JOHNSON" in text
    assert "Python" in text
    assert "Machine Learning" in text


def test_docx_extraction():
    path = Path("data/sample_data/sample_resume.docx")
    text = extract_text(path)

    assert "ALEX JOHNSON" in text
    assert "Python" in text
    assert "Machine Learning" in text
