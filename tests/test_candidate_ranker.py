
import pytest

from src.candidate_ranker import rank_candidates


@pytest.fixture
def job():
    return {
        "raw_text": "Python machine learning SQL developer",
        "skills": {
            "required_skills": ["python", "sql"]
        },
        "minimum_experience_years": 2,
        "education": {
            "qualifications": []
        }
    }


@pytest.fixture
def candidates():
    return [
        {
            "file_name": "candidate_a.pdf",
            "skills": ["python", "sql", "machine learning"],
            "processed_text": "python machine learning sql developer",
            "experience": {"total_experience_years": 4},
            "education": {"qualifications": []}
        },
        {
            "file_name": "candidate_b.pdf",
            "skills": ["python"],
            "processed_text": "python beginner developer",
            "experience": {"total_experience_years": 1},
            "education": {"qualifications": []}
        },
        {
            "file_name": "candidate_c.pdf",
            "skills": ["python", "sql"],
            "processed_text": "python sql software developer",
            "experience": {"total_experience_years": 2},
            "education": {"qualifications": []}
        }
    ]


def test_candidates_are_ranked_highest_first(candidates, job):
    results = rank_candidates(candidates, job)

    scores = [item["overall_score"] for item in results]

    assert scores == sorted(scores, reverse=True)


def test_rank_numbers_are_sequential(candidates, job):
    results = rank_candidates(candidates, job)

    ranks = [item["rank"] for item in results]

    assert ranks == [1, 2, 3]


def test_best_candidate_is_ranked_first(candidates, job):
    results = rank_candidates(candidates, job)

    assert results[0]["file_name"] == "candidate_a.pdf"


def test_empty_candidates_returns_empty_list(job):
    assert rank_candidates([], job) == []


def test_invalid_candidates_type_raises_error(job):
    with pytest.raises(TypeError):
        rank_candidates("invalid", job)


def test_invalid_candidate_raises_error(job):
    with pytest.raises(TypeError):
        rank_candidates(["invalid"], job)


def test_insufficient_data_candidate_has_no_rank(job):
    candidates = [
        {
            "file_name": "candidate_unknown.pdf",
            "skills": [],
            "processed_text": "",
            "experience": {},
            "education": {"qualifications": []}
        }
    ]

    results = rank_candidates(candidates, job)

    assert results[0]["status"] == "insufficient_data"
    assert results[0]["overall_score"] is None
    assert results[0]["rank"] is None


def test_insufficient_data_candidates_appear_last(job):
    candidates = [
        {
            "file_name": "candidate_unknown.pdf",
            "skills": [],
            "processed_text": "",
            "experience": {},
            "education": {"qualifications": []}
        },
        {
            "file_name": "candidate_good.pdf",
            "skills": ["python", "sql"],
            "processed_text": "python sql developer",
            "experience": {"total_experience_years": 3},
            "education": {"qualifications": []}
        }
    ]

    results = rank_candidates(candidates, job)

    assert results[0]["file_name"] == "candidate_good.pdf"
    assert results[1]["file_name"] == "candidate_unknown.pdf"
    assert results[1]["rank"] is None
