
from pathlib import Path

import pytest

from src.document_processor import extract_text


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        extract_text("missing_resume.pdf")


def test_unsupported_file(tmp_path):
    file_path = tmp_path / "resume.txt"
    file_path.write_text("Sample resume")

    with pytest.raises(ValueError, match="Unsupported file format"):
        extract_text(file_path)
