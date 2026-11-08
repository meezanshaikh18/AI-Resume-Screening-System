
from pathlib import Path

import pymupdf
from docx import Document


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def extract_text_from_pdf(file_path: str | Path) -> str:
    """Extract text from a PDF document."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    text_parts = []

    with pymupdf.open(file_path) as pdf:
        for page in pdf:
            text_parts.append(page.get_text("text"))

    return "\n".join(text_parts).strip()


def extract_text_from_docx(file_path: str | Path) -> str:
    """Extract text from a DOCX document."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    document = Document(file_path)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs).strip()


def extract_text(file_path: str | Path) -> str:
    """Extract text based on the document extension."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif extension == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError(
            f"Unsupported file format: {extension}. "
            "Supported formats: PDF and DOCX."
        )

    if not text:
        raise ValueError(
            f"No readable text found in document: {file_path.name}"
        )

    return text
