
import re

from src.skill_extractor import (
    extract_skills,
    SKILL_DATABASE,
)
from src.education_extractor import extract_education


def extract_experience_requirement(text: str) -> float | None:
    """Extract minimum years of experience from job description."""

    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+experience",
        r"minimum\s+of\s+(\d+(?:\.\d+)?)\s+years?",
        r"at\s+least\s+(\d+(?:\.\d+)?)\s+years?",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return float(match.group(1))

    return None


def extract_job_title(text: str) -> str | None:
    """Extract a job title from a Job Title or Position heading."""

    pattern = r"(?:job\s+title|position|role)\s*:\s*([^\n]+)"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return None


def extract_required_and_preferred_skills(
    text: str,
) -> dict:
    """Identify skills in required and preferred sections."""

    required_skills = set()
    preferred_skills = set()

    lines = text.splitlines()
    current_section = "general"

    required_keywords = [
        "required skills",
        "requirements",
        "must have",
        "mandatory skills",
    ]

    preferred_keywords = [
        "preferred skills",
        "nice to have",
        "good to have",
        "desirable skills",
    ]

    for line in lines:
        normalized = line.strip().lower()

        if not normalized:
            continue

        if any(keyword in normalized for keyword in required_keywords):
            current_section = "required"

            content = re.split(r":", line, maxsplit=1)

            if len(content) > 1 and content[1].strip():
                required_skills.update(extract_skills(content[1]))

            continue

        if any(keyword in normalized for keyword in preferred_keywords):
            current_section = "preferred"

            content = re.split(r":", line, maxsplit=1)

            if len(content) > 1 and content[1].strip():
                preferred_skills.update(extract_skills(content[1]))

            continue

        if normalized.endswith(":"):
            current_section = "general"
            continue

        found = extract_skills(line)

        if current_section == "required":
            required_skills.update(found)

        elif current_section == "preferred":
            preferred_skills.update(found)

    all_skills = set(extract_skills(text))

    classified_skills = required_skills | preferred_skills

    general_skills = all_skills - classified_skills

    return {
        "required_skills": sorted(required_skills),
        "preferred_skills": sorted(preferred_skills),
        "general_skills": sorted(general_skills),
        "all_skills": sorted(all_skills),
    }


def parse_job_description(text: str) -> dict:
    """Generate a structured job requirement profile."""

    if not isinstance(text, str):
        raise TypeError("Job description must be a string.")

    if not text.strip():
        raise ValueError("Job description cannot be empty.")

    skills = extract_required_and_preferred_skills(text)

    education = extract_education(text)

    experience = extract_experience_requirement(text)

    job_title = extract_job_title(text)

    return {
        "job_title": job_title,
        "raw_text": text,
        "skills": skills,
        "minimum_experience_years": experience,
        "education": education,
    }
