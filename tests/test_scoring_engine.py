
import pytest

from src.scoring_engine import calculate_candidate_score


def sample_candidate():
    return {
        "skills": ["python", "sql", "machine learning"],
        "processed_text": (
            "python developer machine learning sql "
            "software development"
        ),
        "experience": {
            "total_experience_years": 3
        },
        "education": {
            "qualifications": ["bca"]
        },
    }


def sample_job():
    return {
        "raw_text": (
            "python machine learning sql developer "
            "software engineering"
        ),
        "skills": {
            "required_skills": ["python", "sql"]
        },
        "minimum_experience_years": 2,
        "education": {
            "qualifications": []
        },
    }


def test_candidate_score_calculated():
    result = calculate_candidate_score(
        sample_candidate(),
        sample_job(),
    )

    assert result["status"] == "calculated"
    assert 0 <= result["overall_score"] <= 100


def test_missing_education_is_excluded():
    result = calculate_candidate_score(
        sample_candidate(),
        sample_job(),
    )

    assert "education" not in result["components"]


def test_weights_are_normalized():
    result = calculate_candidate_score(
        sample_candidate(),
        sample_job(),
    )

    assert sum(result["active_weights"].values()) == pytest.approx(1.0)


def test_no_evaluable_criteria():
    candidate = {"skills": []}
    job = {"skills": {"required_skills": []}}

    result = calculate_candidate_score(candidate, job)

    assert result["overall_score"] is None
    assert result["status"] == "insufficient_data"


def test_invalid_weights():
    with pytest.raises(ValueError):
        calculate_candidate_score(
            sample_candidate(),
            sample_job(),
            {"skills": -1, "text_similarity": 0.3,
             "experience": 0.2, "education": 0.1},
        )
