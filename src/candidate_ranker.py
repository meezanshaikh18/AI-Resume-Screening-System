
from src.scoring_engine import calculate_candidate_score


def rank_candidates(candidates, job, weights=None):
    """
    Calculate scores and rank candidates against a job description.

    Args:
        candidates (list): List of parsed candidate profiles.
        job (dict): Parsed job description.
        weights (dict, optional): Custom scoring weights.

    Returns:
        list: Candidates sorted by score, highest first.
    """

    if not isinstance(candidates, list):
        raise TypeError("Candidates must be provided as a list.")

    if not candidates:
        return []

    ranked_candidates = []

    for candidate in candidates:

        if not isinstance(candidate, dict):
            raise TypeError("Each candidate must be a dictionary.")

        score_result = calculate_candidate_score(
            candidate,
            job,
            weights=weights
        )

        ranked_candidates.append({
            "file_name": candidate.get("file_name", "Unknown"),
            "overall_score": score_result["overall_score"],
            "status": score_result["status"],
            "component_scores": score_result["components"],
            "active_weights": score_result["active_weights"]
        })

    # Candidates with calculated scores come first.
    # Candidates with insufficient data remain at the bottom.
    ranked_candidates.sort(
        key=lambda candidate: (
            candidate["overall_score"] is not None,
            candidate["overall_score"] if candidate["overall_score"] is not None else -1
        ),
        reverse=True
    )

    # Assign ranks only to candidates with calculated scores.
    rank = 0

    for candidate in ranked_candidates:
        if candidate["overall_score"] is not None:
            rank += 1
            candidate["rank"] = rank
        else:
            candidate["rank"] = None

    return ranked_candidates
