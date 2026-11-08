
import csv
import pytest

from src.report_generator import generate_csv_report


@pytest.fixture
def ranked_candidates():
    return [
        {
            "file_name": "candidate_a.pdf",
            "overall_score": 95.5,
            "status": "calculated",
            "rank": 1,
            "component_scores": {
                "skills": {
                    "score": 100.0,
                    "matched_skills": ["python", "sql"],
                    "missing_skills": [],
                },
                "text_similarity": 90.0,
                "experience": 95.0,
            },
            "active_weights": {
                "skills": 0.4444,
                "text_similarity": 0.3333,
                "experience": 0.2222,
            },
        },
        {
            "file_name": "candidate_b.pdf",
            "overall_score": None,
            "status": "insufficient_data",
            "rank": None,
            "component_scores": {},
            "active_weights": {},
        },
    ]


def test_generate_csv_report(ranked_candidates, tmp_path):
    output_file = tmp_path / "reports" / "ranking.csv"

    result = generate_csv_report(
        ranked_candidates,
        str(output_file),
        "Python Developer",
    )

    assert output_file.exists()
    assert result == str(output_file.resolve())


def test_csv_contains_all_candidates(ranked_candidates, tmp_path):
    output_file = tmp_path / "ranking.csv"

    generate_csv_report(ranked_candidates, str(output_file))

    with output_file.open(
        encoding="utf-8-sig",
        newline="",
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 2
    assert rows[0]["Candidate"] == "candidate_a.pdf"
    assert rows[1]["Candidate"] == "candidate_b.pdf"


def test_csv_contains_skill_details(ranked_candidates, tmp_path):
    output_file = tmp_path / "ranking.csv"

    generate_csv_report(ranked_candidates, str(output_file))

    with output_file.open(
        encoding="utf-8-sig",
        newline="",
    ) as file:
        rows = list(csv.DictReader(file))

    assert rows[0]["Matched Skills"] == "python, sql"
    assert rows[0]["Missing Skills"] == ""
    assert rows[0]["Skills Score (%)"] == "100.0"


def test_csv_contains_job_title(ranked_candidates, tmp_path):
    output_file = tmp_path / "ranking.csv"

    generate_csv_report(
        ranked_candidates,
        str(output_file),
        "Python Developer",
    )

    with output_file.open(
        encoding="utf-8-sig",
        newline="",
    ) as file:
        rows = list(csv.DictReader(file))

    assert rows[0]["Job Title"] == "Python Developer"


def test_empty_candidates_raises_error(tmp_path):
    with pytest.raises(ValueError):
        generate_csv_report([], str(tmp_path / "empty.csv"))


def test_invalid_candidates_type_raises_error(tmp_path):
    with pytest.raises(TypeError):
        generate_csv_report("invalid", str(tmp_path / "invalid.csv"))


def test_invalid_file_extension_raises_error(ranked_candidates, tmp_path):
    with pytest.raises(ValueError):
        generate_csv_report(
            ranked_candidates,
            str(tmp_path / "report.txt"),
        )


def test_missing_component_scores_are_handled(tmp_path):
    candidates = [
        {
            "file_name": "candidate_unknown.pdf",
            "overall_score": None,
            "status": "insufficient_data",
            "rank": None,
        }
    ]

    output_file = tmp_path / "ranking.csv"

    generate_csv_report(candidates, str(output_file))

    with output_file.open(
        encoding="utf-8-sig",
        newline="",
    ) as file:
        rows = list(csv.DictReader(file))

    assert rows[0]["Skills Score (%)"] == ""
    assert rows[0]["Evaluation Status"] == "insufficient_data"
