
import csv
from pathlib import Path
from datetime import datetime


def generate_csv_report(
    ranked_candidates: list,
    output_path: str,
    job_title: str = "Untitled Position",
) -> str:
    """
    Generate a recruiter-friendly CSV report.

    Args:
        ranked_candidates: Output from rank_candidates().
        output_path: Destination CSV file path.
        job_title: Job title associated with the report.

    Returns:
        str: Path to the generated CSV report.
    """

    if not isinstance(ranked_candidates, list):
        raise TypeError("Ranked candidates must be provided as a list.")

    if not ranked_candidates:
        raise ValueError("Cannot generate a report without candidates.")

    output_file = Path(output_path)

    if output_file.suffix.lower() != ".csv":
        raise ValueError("Output file must have a .csv extension.")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "Job Title",
        "Report Generated",
        "Rank",
        "Candidate",
        "Overall Score (%)",
        "Skills Score (%)",
        "Matched Skills",
        "Missing Skills",
        "Text Similarity (%)",
        "Experience Score (%)",
        "Education Score (%)",
        "Evaluation Status",
    ]

    with output_file.open(
        mode="w",
        newline="",
        encoding="utf-8-sig",
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for candidate in ranked_candidates:
            components = candidate.get("component_scores", {})

            skills = components.get("skills", {})

            writer.writerow({
                "Job Title": job_title,
                "Report Generated": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Rank": candidate.get("rank"),
                "Candidate": candidate.get("file_name", "Unknown"),
                "Overall Score (%)": candidate.get("overall_score"),
                "Skills Score (%)": skills.get("score"),
                "Matched Skills": ", ".join(
                    skills.get("matched_skills", [])
                ),
                "Missing Skills": ", ".join(
                    skills.get("missing_skills", [])
                ),
                "Text Similarity (%)": components.get(
                    "text_similarity"
                ),
                "Experience Score (%)": components.get(
                    "experience"
                ),
                "Education Score (%)": components.get(
                    "education"
                ),
                "Evaluation Status": candidate.get("status"),
            })

    return str(output_file.resolve())
