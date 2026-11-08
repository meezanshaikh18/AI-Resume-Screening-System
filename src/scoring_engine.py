
from src.matching_engine import (
    calculate_skill_match,
    calculate_text_similarity,
    calculate_experience_match,
    calculate_education_match,
)


DEFAULT_WEIGHTS = {
    "skills": 0.40,
    "text_similarity": 0.30,
    "experience": 0.20,
    "education": 0.10,
}


def calculate_candidate_score(
    candidate: dict,
    job: dict,
    weights: dict | None = None,
) -> dict:
    """Calculate an explainable candidate-job match score."""

    weights = DEFAULT_WEIGHTS.copy() if weights is None else weights

    if set(weights) != set(DEFAULT_WEIGHTS):
        raise ValueError("Weights must contain exactly the four criteria.")

    if any(not isinstance(v, (int, float)) or v < 0 for v in weights.values()):
        raise ValueError("Weights must be non-negative numbers.")

    if sum(weights.values()) <= 0:
        raise ValueError("At least one weight must be positive.")

    components = {}
    active_weights = {}

    # Required skills
    required_skills = job.get("skills", {}).get(
        "required_skills", []
    )

    candidate_has_skill_evidence = (
        bool(candidate.get("skills"))
        or bool(candidate.get("processed_text", "").strip())
    )

    if required_skills and candidate_has_skill_evidence:
        result = calculate_skill_match(
            candidate.get("skills", []),
            required_skills,
        )

        components["skills"] = result
        active_weights["skills"] = weights["skills"]

    # Text similarity
    candidate_text = candidate.get("processed_text", "")
    job_text = job.get("raw_text", "")

    if candidate_text.strip() and job_text.strip():
        similarity = calculate_text_similarity(
            candidate_text,
            job_text,
        )

        components["text_similarity"] = similarity
        active_weights["text_similarity"] = weights["text_similarity"]

    # Experience
    required_years = job.get("minimum_experience_years")
    candidate_experience = candidate.get("experience", {})

    if (
        required_years is not None
        and "total_experience_years" in candidate_experience
        and candidate_experience["total_experience_years"] is not None
    ):
        candidate_years = candidate_experience["total_experience_years"]

        components["experience"] = calculate_experience_match(
            candidate_years,
            required_years,
        )

        active_weights["experience"] = weights["experience"]

    # Education
    required_education = job.get(
        "education", {}
    ).get("qualifications", [])

    if required_education:
        candidate_education = candidate.get(
            "education", {}
        ).get("qualifications", [])

        components["education"] = calculate_education_match(
            candidate_education,
            required_education,
        )

        active_weights["education"] = weights["education"]

    # Calculate final score
    total_weight = sum(active_weights.values())

    if total_weight == 0:
        return {
            "overall_score": None,
            "components": components,
            "active_weights": active_weights,
            "status": "insufficient_data",
        }

    weighted_score = 0.0

    for criterion, weight in active_weights.items():
        value = components[criterion]

        if criterion == "skills":
            value = value["score"]

        weighted_score += value * weight

    final_score = weighted_score / total_weight

    return {
        "overall_score": round(final_score, 2),
        "components": components,
        "active_weights": {
            key: value / total_weight
            for key, value in active_weights.items()
        },
        "status": "calculated",
    }
