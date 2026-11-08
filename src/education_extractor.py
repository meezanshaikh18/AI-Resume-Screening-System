
import re


EDUCATION_DATABASE = {
    "doctorate": [
        "phd",
        "ph.d",
        "doctor of philosophy",
    ],
    "masters": [
        "m.tech",
        "mtech",
        "master of computer application",
        "master of technology",
        "mca",
        "master of computer applications",
        "mba",
        "master of business administration",
        "m.sc",
        "msc",
        "master of science",
        "m.com",
        "master of commerce",
        "ma",
        "master of arts",
    ],
    "bachelors": [
        "b.tech",
        "btech",
        "bachelor of technology",
        "b.e",
        "b.e.",
        "bachelor of engineering",
        "bca",
        "bachelor of computer applications",
        "b.sc",
        "bsc",
        "bachelor of science",
        "b.com",
        "bachelor of commerce",
        "bba",
        "bachelor of business administration",
        "b.a",
        "bachelor of arts",
    ],
    "diploma": [
        "diploma",
        "polytechnic",
    ],
}


def extract_education(text: str) -> dict:
    """Identify recognized educational qualifications."""

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    text_lower = text.lower()

    results = {}

    for category, qualifications in EDUCATION_DATABASE.items():
        found = []

        for qualification in qualifications:
            pattern = (
                r"(?<!\w)"
                + re.escape(qualification)
                + r"(?!\w)"
            )

            if re.search(pattern, text_lower):
                found.append(qualification)

        results[category] = sorted(set(found))

    all_qualifications = sorted({
        qualification
        for qualifications in results.values()
        for qualification in qualifications
    })

    return {
        "qualifications": all_qualifications,
        "qualifications_by_level": results,
    }
