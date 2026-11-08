
import re
from datetime import date


MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}


DATE_PATTERN = (
    r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|"
    r"Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|"
    r"Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
    r"\s+(\d{4})"
    r"\s*(?:-|–|—|to)\s*"
    r"(Present|Current|"
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|"
    r"May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|"
    r"Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|"
    r"Dec(?:ember)?)\s+\d{4})"
)


def _parse_month_year(value: str) -> tuple[int, int]:
    """Convert a month-year string into numeric month and year."""

    parts = value.lower().split()

    month = MONTHS[parts[0]]
    year = int(parts[1])

    return year, month


def extract_experience(text: str) -> dict:
    """
    Extract employment date ranges and estimate total experience.

    This initial version uses month-year date ranges.
    It does not infer experience from education dates.
    """

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    matches = re.finditer(DATE_PATTERN, text, re.IGNORECASE)

    entries = []

    for match in matches:
        start_month_name = match.group(1)
        start_year = int(match.group(2))
        end_value = match.group(3)

        start_month = MONTHS[start_month_name.lower()]

        start_index = start_year * 12 + start_month

        if end_value.lower() in {"present", "current"}:
            end_date = date.today()
            end_year = end_date.year
            end_month = end_date.month
            is_current = True
        else:
            end_year, end_month = _parse_month_year(end_value)
            is_current = False

        end_index = end_year * 12 + end_month

        if end_index < start_index:
            continue

        duration_months = end_index - start_index

        entries.append({
            "start_date": f"{start_month_name} {start_year}",
            "end_date": end_value,
            "is_current": is_current,
            "duration_months": duration_months,
        })

    # Merge overlapping date ranges to avoid double counting.
    intervals = []

    for entry in entries:
        start_year, start_month = _parse_month_year(
            entry["start_date"]
        )

        end_year, end_month = (
            (date.today().year, date.today().month)
            if entry["is_current"]
            else _parse_month_year(entry["end_date"])
        )

        intervals.append((
            start_year * 12 + start_month,
            end_year * 12 + end_month,
        ))

    intervals.sort()

    total_months = 0

    if intervals:
        current_start, current_end = intervals[0]

        for start, end in intervals[1:]:
            if start <= current_end:
                current_end = max(current_end, end)
            else:
                total_months += current_end - current_start
                current_start, current_end = start, end

        total_months += current_end - current_start

    return {
        "experience_entries": entries,
        "total_experience_months": total_months,
        "total_experience_years": round(total_months / 12, 2),
    }
