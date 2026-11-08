
from pathlib import Path

from src.document_processor import extract_text
from src.text_preprocessor import clean_text, preprocess_text
from src.skill_extractor import (
    extract_skills,
    extract_skills_by_category,
)
from src.experience_extractor import extract_experience
from src.education_extractor import extract_education


def parse_resume(file_path: str | Path) -> dict:
    """Extract a structured candidate profile from a resume."""

    file_path = Path(file_path)

    # Extract document text.
    raw_text = extract_text(file_path)

    # Preprocess text.
    cleaned_text = clean_text(raw_text)
    processed_text = preprocess_text(cleaned_text)

    # Extract technical skills.
    skills = extract_skills(raw_text)
    skills_by_category = extract_skills_by_category(raw_text)

    # Extract experience information.
    experience = extract_experience(raw_text)

    # Extract educational qualifications.
    education = extract_education(raw_text)

    return {
        "file_name": file_path.name,
        "file_type": file_path.suffix.lower(),
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "processed_text": processed_text,
        "skills": skills,
        "skills_by_category": skills_by_category,
        "experience": experience,
        "education": education,
    }
