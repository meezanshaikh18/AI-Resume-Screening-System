
import re

from src.skill_extractor import extract_skills
from src.education_extractor import extract_education


def extract_experience_requirement(text: str) -> float | None:
    """Extract minimum years of experience from a job description."""

    patterns = [
        # Experience Required: 5+ years
        r"experience\s*(?:required|needed|level)?\s*[:\-]\s*(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",

        # Minimum 5 years / Minimum of 5 years
        r"minimum\s+(?:of\s+)?(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",

        # At least 5 years
        r"at\s+least\s+(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",

        # 5+ years of experience
        r"(\d+(?:\.\d+)?)\s*\+\s*(?:years?|yrs?)\s+of\s+(?:(?:relevant|professional)\s+)*experience",

        # 5 years of relevant professional experience
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s+of\s+(?:(?:relevant|professional)\s+)*experience",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return float(match.group(1))

    return None


def extract_job_title(text: str) -> str | None:
    """
    Extract a job title from:
    1. Explicit labels such as Job Title: or Position:
    2. The first meaningful heading in the job description.
    """

    explicit_pattern = (
        r"(?:job\s+title|position|role)"
        r"\s*[:\-]\s*([^\n]+)"
    )

    match = re.search(explicit_pattern, text, re.IGNORECASE)

    if match:
        title = match.group(1).strip()
        title = re.sub(r"[*#`]", "", title).strip()

        if title:
            return title

    # Fallback: use the first meaningful line as the job title.
    ignored_headings = {
        "job description",
        "job details",
        "job overview",
        "about the job",
        "about the role",
        "company",
        "department",
        "employment type",
        "experience required",
    }

    for line in text.splitlines():
        cleaned = re.sub(r"^\s*#+\s*", "", line)
        cleaned = re.sub(r"^\s*[-*•]\s*", "", cleaned)
        cleaned = re.sub(r"[*#`]", "", cleaned)
        cleaned = cleaned.strip()

        if not cleaned:
            continue

        normalized = cleaned.lower().rstrip(":")

        if normalized in ignored_headings:
            continue

        if re.match(
            r"^(company|department|employment\s+type|work\s+mode|"
            r"experience\s+required)\s*:",
            cleaned,
            re.IGNORECASE,
        ):
            continue

        return cleaned

    return None


def extract_required_and_preferred_skills(text: str) -> dict:
    """Identify required, preferred, and general skills."""

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

        # Stop collecting skills when a new section begins.
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
