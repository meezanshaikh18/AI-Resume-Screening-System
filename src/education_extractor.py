
import re


EDUCATION_DATABASE = {
    "doctorate": [
        "phd",
        "ph.d",
        "doctor of philosophy",
    ],
    "masters": [
        "m.tech",
        "mtech",
        "master of computer application",
        "master of technology",
        "mca",
        "master of computer applications",
        "master of business administration",
        "mba",
        "m.sc",
        "msc",
        "master of science",
        "m.com",
        "master of commerce",
        "ma",
        "master of arts",
        "master of computer science",
    ],
    "bachelors": [
        "b.tech",
        "btech",
        "bachelor of technology",
        "b.e",
        "b.e.",
        "bachelor of engineering",
        "bca",
        "bachelor of computer applications",
        "b.sc",
        "bsc",
        "bachelor of science",
        "b.com",
        "bachelor of commerce",
        "bba",
        "bachelor of business administration",
        "b.a",
        "bachelor of arts",
        "bachelor of computer science",
    ],
    "diploma": [
        "diploma",
        "polytechnic",
    ],
}


# Generic degree-level phrases commonly found in job descriptions.
GENERIC_DEGREE_PATTERNS = {
    "doctorate": [
        r"\bdoctorate\b",
        r"\bdoctoral degree\b",
        r"\bph\.?\s*d\.?\b",
    ],
    "masters": [
        r"\bmaster'?s(?:\s+degree)?\b",
        r"\bpostgraduate degree\b",
        r"\bpost graduate degree\b",
    ],
    "bachelors": [
        r"\bbachelor'?s(?:\s+degree)?\b",
        r"\bundergraduate degree\b",
    ],
    "diploma": [
        r"\bdiploma\b",
        r"\bpolytechnic\b",
    ],
}


FIELD_ALIASES = {
    "computer science": [
        "computer science",
        "computer science and engineering",
        "computer science engineering",
        "cse",
    ],
    "information technology": [
        "information technology",
        "information technology engineering",
    ],
    "computer applications": [
        "computer applications",
        "computer application",
    ],
    "software engineering": [
        "software engineering",
    ],
    "information systems": [
        "information systems",
        "management information systems",
    ],
    "electronics": [
        "electronics",
        "electronics and communication",
        "electronics and communication engineering",
        "ece",
    ],
    "mechanical engineering": [
        "mechanical engineering",
    ],
    "civil engineering": [
        "civil engineering",
    ],
    "electrical engineering": [
        "electrical engineering",
    ],
    "data science": [
        "data science",
        "data analytics",
    ],
    "mathematics": [
        "mathematics",
        "applied mathematics",
    ],
    "physics": [
        "physics",
    ],
    "chemistry": [
        "chemistry",
    ],
    "business administration": [
        "business administration",
        "business management",
    ],
    "commerce": [
        "commerce",
    ],
    "arts": [
        "arts",
    ],
}


# Fields that are closely related for this project's initial matching rules.
RELATED_FIELD_GROUPS = [
    {
        "computer science",
        "information technology",
        "computer applications",
        "software engineering",
        "information systems",
    },
]


def _contains_phrase(text: str, phrase: str) -> bool:
    """Check for a phrase without matching it inside another word."""

    pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
    return re.search(pattern, text, re.IGNORECASE) is not None


def extract_fields_of_study(text: str) -> list[str]:
    """Extract recognized fields of study from educational text."""

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    text_lower = text.lower()
    found_fields = set()

    for canonical_field, aliases in FIELD_ALIASES.items():
        for alias in aliases:
            if _contains_phrase(text_lower, alias):
                found_fields.add(canonical_field)
                break

    return sorted(found_fields)


def extract_education(text: str) -> dict:
    """
    Extract educational qualifications, degree levels and fields.

    Existing output keys are preserved for compatibility.
    Additional structured fields provide evidence for education matching.
    """

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    text_lower = text.lower()

    qualifications_by_level = {}
    qualification_entries = []

    for level, qualifications in EDUCATION_DATABASE.items():
        found = []

        for qualification in qualifications:
            if _contains_phrase(text_lower, qualification):
                found.append(qualification)

        qualifications_by_level[level] = sorted(set(found))

        for qualification in sorted(set(found)):
            inferred_fields = []

            # Infer fields directly from the recognized degree title.
            if "computer application" in qualification:
                inferred_fields.append("computer applications")
            elif "computer science" in qualification:
                inferred_fields.append("computer science")
            elif "business administration" in qualification:
                inferred_fields.append("business administration")
            elif "engineering" in qualification or qualification in {
                "m.tech", "mtech", "b.tech", "btech", "mca", "bca"
            }:
                if qualification in {"mca", "master of computer application",
                                     "master of computer applications",
                                     "bca", "bachelor of computer applications"}:
                    inferred_fields.append("computer applications")

            qualification_entries.append({
                "qualification": qualification,
                "level": level,
                "fields_of_study": sorted(set(inferred_fields)),
            })

    # Recognize generic degree requirements, especially in job descriptions.
    for level, patterns in GENERIC_DEGREE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                generic_label = f"{level} degree"

                if generic_label not in qualifications_by_level[level]:
                    qualifications_by_level[level].append(generic_label)

                qualification_entries.append({
                    "qualification": generic_label,
                    "level": level,
                    "fields_of_study": [],
                })

    for level in qualifications_by_level:
        qualifications_by_level[level] = sorted(
            set(qualifications_by_level[level])
        )

    # Extract known fields separately.
    fields_of_study = extract_fields_of_study(text)

    # Attach recognized fields to entries when the degree title did not
    # already provide a more specific field.
    for entry in qualification_entries:
        if not entry["fields_of_study"]:
            entry["fields_of_study"] = fields_of_study.copy()

    all_qualifications = sorted({
        qualification
        for qualifications in qualifications_by_level.values()
        for qualification in qualifications
    })

    return {
        "qualifications": all_qualifications,
        "qualifications_by_level": qualifications_by_level,
        "fields_of_study": fields_of_study,
        "qualification_entries": qualification_entries,
    }
