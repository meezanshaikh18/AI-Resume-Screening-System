
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

    Supports structured education evaluation while preserving
    compatibility with older numeric education scores.
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
        "Education Status",
        "Degree Level Match",
        "Field Match",
        "Matched Degree Levels",
        "Exact Field Matches",
        "Related Field Matches",
        "Missing Required Fields",
        "Education Explanation",
        "Evaluation Status",
    ]

    report_generated = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

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

            skills = components.get("skills") or {}
            education = components.get("education")

            # Handle structured education results.
            if isinstance(education, dict):
                education_score = education.get("score")
                education_status = education.get("status")

                degree_level_match = education.get(
                    "degree_level_match"
                )

                field_match = education.get("field_match")

                matched_levels = education.get(
                    "matched_levels", []
                )

                exact_fields = education.get(
                    "exact_field_matches", []
                )

                related_fields = education.get(
                    "related_field_matches", []
                )

                missing_fields = education.get(
                    "missing_fields", []
                )

                education_explanation = education.get(
                    "explanation", ""
                )

                related_fields_text = "; ".join(
                    (
                        f"{item.get('candidate_field', 'Unknown')} "
                        f"-> {item.get('required_field', 'Unknown')}"
                    )
                    for item in related_fields
                    if isinstance(item, dict)
                )

            # Backward compatibility with numeric education scores.
            elif isinstance(education, (int, float)):
                education_score = education
                education_status = "legacy_numeric_result"
                degree_level_match = ""
                field_match = ""
                matched_levels = []
                exact_fields = []
                related_fields_text = ""
                missing_fields = []
                education_explanation = ""

            else:
                education_score = None
                education_status = "insufficient_data"
                degree_level_match = ""
                field_match = ""
                matched_levels = []
                exact_fields = []
                related_fields_text = ""
                missing_fields = []
                education_explanation = ""

            writer.writerow({
                "Job Title": job_title,
                "Report Generated": report_generated,
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

                # Numeric education score, not the entire dictionary.
                "Education Score (%)": education_score,
                "Education Status": education_status,
                "Degree Level Match": degree_level_match,
                "Field Match": field_match,

                "Matched Degree Levels": ", ".join(matched_levels),
                "Exact Field Matches": ", ".join(exact_fields),
                "Related Field Matches": related_fields_text,
                "Missing Required Fields": ", ".join(missing_fields),
                "Education Explanation": education_explanation,

                "Evaluation Status": candidate.get("status"),
            })

    return str(output_file.resolve())
