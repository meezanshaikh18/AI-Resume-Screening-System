
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


RELATED_FIELD_GROUPS = [
    {
        "computer science",
        "information technology",
        "computer applications",
        "software engineering",
        "information systems",
    },
]


DEGREE_LEVELS = {
    "doctorate": 4,
    "masters": 3,
    "bachelors": 2,
    "diploma": 1,
}


def calculate_skill_match(
    candidate_skills: list[str],
    required_skills: list[str],
) -> dict:
    """Calculate required skill coverage."""

    candidate_set = {skill.lower() for skill in candidate_skills}
    required_set = {skill.lower() for skill in required_skills}

    if not required_set:
        return {
            "score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
        }

    matched = sorted(candidate_set & required_set)
    missing = sorted(required_set - candidate_set)

    score = len(matched) / len(required_set) * 100

    return {
        "score": round(score, 2),
        "matched_skills": matched,
        "missing_skills": missing,
    }


def calculate_text_similarity(
    candidate_text: str,
    job_description: str,
) -> float:
    """Calculate TF-IDF cosine similarity."""

    if not candidate_text.strip() or not job_description.strip():
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
    )

    try:
        vectors = vectorizer.fit_transform([
            candidate_text,
            job_description,
        ])

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2],
        )[0][0]

        return round(float(similarity * 100), 2)

    except ValueError:
        return 0.0


def calculate_experience_match(
    candidate_years: float,
    required_years: float | None,
) -> float:
    """Compare candidate experience with the job requirement."""

    if required_years is None or required_years <= 0:
        return 0.0

    if candidate_years < 0:
        raise ValueError("Candidate experience cannot be negative.")

    score = min(candidate_years / required_years, 1.0) * 100

    return round(score, 2)


def _normalize_education(education):
    """Support legacy lists and structured education dictionaries."""

    if isinstance(education, list):
        return {
            "qualifications": education,
            "qualifications_by_level": {},
            "fields_of_study": [],
        }

    if not isinstance(education, dict):
        return {
            "qualifications": [],
            "qualifications_by_level": {},
            "fields_of_study": [],
        }

    return {
        "qualifications": education.get("qualifications", []),
        "qualifications_by_level": education.get(
            "qualifications_by_level", {}
        ),
        "fields_of_study": education.get("fields_of_study", []),
    }


def _get_degree_levels(education):
    """Identify degree levels from structured or legacy qualifications."""

    levels = set()

    for level, qualifications in education[
        "qualifications_by_level"
    ].items():
        if qualifications:
            levels.add(level)

    if levels:
        return levels

    qualification_text = " ".join(
        str(item).lower()
        for item in education["qualifications"]
    )

    aliases = {
        "doctorate": [
            "phd",
            "ph.d",
            "doctor of philosophy",
        ],
        "masters": [
            "mca",
            "mba",
            "msc",
            "m.sc",
            "mtech",
            "m.tech",
            "master",
            "masters",
        ],
        "bachelors": [
            "bca",
            "bba",
            "bsc",
            "b.sc",
            "btech",
            "b.tech",
            "bachelor",
            "bachelors",
        ],
        "diploma": [
            "diploma",
            "polytechnic",
        ],
    }

    for level, terms in aliases.items():
        if any(term in qualification_text for term in terms):
            levels.add(level)

    return levels


def _get_field_match_details(candidate_fields, required_fields):
    """Return exact and related field matches separately."""

    candidate_set = set(candidate_fields)
    required_set = set(required_fields)

    exact_matches = sorted(candidate_set & required_set)
    related_matches = []

    for group in RELATED_FIELD_GROUPS:
        candidate_group_fields = candidate_set & group
        required_group_fields = required_set & group

        if candidate_group_fields and required_group_fields:
            for candidate_field in sorted(candidate_group_fields):
                for required_field in sorted(required_group_fields):
                    if candidate_field != required_field:
                        related_matches.append({
                            "candidate_field": candidate_field,
                            "required_field": required_field,
                        })

    matched_required_fields = set(exact_matches)

    matched_required_fields.update(
        item["required_field"]
        for item in related_matches
    )

    return {
        "is_match": bool(matched_required_fields),
        "exact_matches": exact_matches,
        "related_matches": related_matches,
        "missing_fields": sorted(
            required_set - matched_required_fields
        ),
    }


def calculate_education_match_details(
    candidate_qualifications,
    required_qualifications,
) -> dict:
    """
    Return detailed education matching results.

    This is a transparent rule-based estimate, not an accreditation
    or formal qualification-equivalency determination.
    """

    candidate = _normalize_education(candidate_qualifications)
    required = _normalize_education(required_qualifications)

    candidate_levels = _get_degree_levels(candidate)
    required_levels = _get_degree_levels(required)

    candidate_fields = set(candidate["fields_of_study"])
    required_fields = set(required["fields_of_study"])

    field_details = (
        _get_field_match_details(
            candidate_fields,
            required_fields,
        )
        if required_fields
        else None
    )

    field_match = (
        field_details["is_match"]
        if field_details is not None
        else None
    )

    exact_field_matches = (
        field_details["exact_matches"]
        if field_details else []
    )

    related_field_matches = (
        field_details["related_matches"]
        if field_details else []
    )

    missing_fields = (
        field_details["missing_fields"]
        if field_details else []
    )

    matched_fields = sorted(
        set(exact_field_matches)
        | {
            item["candidate_field"]
            for item in related_field_matches
        }
    )

    if not candidate["qualifications"]:
        return {
            "score": None,
            "status": "insufficient_data",
            "degree_level_match": None,
            "field_match": None,
            "matched_levels": [],
            "matched_fields": [],
            "exact_field_matches": [],
            "related_field_matches": [],
            "missing_fields": sorted(required_fields),
            "explanation": (
                "Candidate education information was not detected."
            ),
        }

    if not required["qualifications"]:
        return {
            "score": None,
            "status": "not_required",
            "degree_level_match": None,
            "field_match": None,
            "matched_levels": [],
            "matched_fields": [],
            "exact_field_matches": [],
            "related_field_matches": [],
            "missing_fields": [],
            "explanation": (
                "The job description does not specify an education requirement."
            ),
        }

    matched_levels = sorted(candidate_levels & required_levels)

    degree_level_match = any(
        DEGREE_LEVELS.get(candidate_level, 0)
        >= DEGREE_LEVELS.get(required_level, 0)
        for candidate_level in candidate_levels
        for required_level in required_levels
    )

    if not candidate_levels or not required_levels:
        return {
            "score": None,
            "status": "insufficient_data",
            "degree_level_match": None,
            "field_match": field_match,
            "matched_levels": matched_levels,
            "matched_fields": matched_fields,
            "exact_field_matches": exact_field_matches,
            "related_field_matches": related_field_matches,
            "missing_fields": missing_fields,
            "explanation": (
                "Degree level could not be confidently established."
            ),
        }

    if not degree_level_match:
        score = 0.0
        status = "degree_requirement_not_met"
        explanation = (
            "The detected qualification level does not meet "
            "the specified degree level."
        )

    elif required_fields and not field_match:
        score = 50.0
        status = "degree_match_field_mismatch"
        explanation = (
            "Degree level matches, but the detected field does "
            "not match the required field."
        )

    elif required_fields and related_field_matches:
        score = 100.0
        status = "degree_and_related_field_match"
        explanation = (
            "Degree level matches and the candidate's field is "
            "configured as related to the required field."
        )

    elif required_fields:
        score = 100.0
        status = "degree_and_field_match"
        explanation = (
            "Degree level and field match the stated requirements."
        )

    else:
        score = 100.0
        status = "degree_level_match"
        explanation = (
            "The detected degree level meets the stated requirement."
        )

    return {
        "score": score,
        "status": status,
        "degree_level_match": degree_level_match,
        "field_match": field_match,
        "matched_levels": matched_levels,
        "matched_fields": matched_fields,
        "exact_field_matches": exact_field_matches,
        "related_field_matches": related_field_matches,
        "missing_fields": missing_fields,
        "explanation": explanation,
    }


def calculate_education_match(
    candidate_qualifications,
    required_qualifications,
) -> float:
    """
    Return a numeric education score for backward compatibility.
    """

    result = calculate_education_match_details(
        candidate_qualifications,
        required_qualifications,
    )

    score = result.get("score")

    return 0.0 if score is None else score
