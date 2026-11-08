
import pytest

from src.text_preprocessor import clean_text, preprocess_text


def test_clean_text_lowercase():
    result = clean_text("PYTHON DEVELOPER")
    assert result == "python developer"


def test_clean_text_whitespace():
    result = clean_text("Python     Developer")
    assert result == "python developer"


def test_clean_text_invalid_input():
    with pytest.raises(TypeError):
        clean_text(123)


def test_preprocess_text():
    result = preprocess_text(
        "The developers are building Python applications."
    )

    assert "developer" in result
    assert "build" in result
    assert "application" in result


def test_preprocess_empty_text():
    assert preprocess_text("") == ""
