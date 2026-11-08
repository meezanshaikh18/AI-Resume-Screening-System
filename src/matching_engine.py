
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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


def calculate_education_match(
    candidate_qualifications: list[str],
    required_qualifications: list[str],
) -> float:
    """Compare recognized qualification labels."""

    candidate_set = {
        item.lower() for item in candidate_qualifications
    }

    required_set = {
        item.lower() for item in required_qualifications
    }

    if not required_set:
        return 0.0

    matched = candidate_set & required_set

    return round(
        len(matched) / len(required_set) * 100,
        2,
    )
