
import re
from typing import Iterable



SKILL_DATABASE = {
    "programming_languages": [
        "python",
        "java",
        "javascript",
        "typescript",
        "c",
        "c++",
        "c#",
        "r",
        "sql",
        "php",
    ],

    "frontend_development": [
        "angular",
        "ionic",
        "react",
        "vue",
        "html5",
        "html",
        "css3",
        "css",
        "scss",
        "sass",
        "bootstrap",
        "tailwind css",
        "responsive web design",
    ],

    "mobile_development": [
        "mobile application development",
        "cross-platform mobile application development",
        "push notifications",
        "offline data storage",
        "device plugins",
        "google maps",
    ],

    "backend_and_api": [
        "rest api",
        "rest apis",
        "api integration",
        "jwt authentication",
        "jwt",
        "node.js",
        "express.js",
        "fastapi",
        "flask",
    ],

    "state_management": [
        "ngrx",
        "redux",
        "context api",
    ],

    "machine_learning": [
        "machine learning",
        "deep learning",
        "supervised learning",
        "unsupervised learning",
        "reinforcement learning",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "keras",
        "xgboost",
    ],

    "data_science": [
        "pandas",
        "numpy",
        "scipy",
        "statistics",
        "data analysis",
        "data visualization",
        "matplotlib",
        "seaborn",
        "plotly",
    ],

    "generative_ai": [
        "generative ai",
        "large language models",
        "llm",
        "natural language processing",
        "nlp",
        "computer vision",
        "transformers",
        "hugging face",
        "langchain",
        "rag",
    ],

    "tools_and_platforms": [
        "git",
        "github",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "azure devops",
        "google cloud",
        "bitbucket",
        "mlops",
        "streamlit",
        "ci/cd",
        "continuous integration",
        "continuous deployment",
    ],

    "databases": [
        "mysql",
        "postgresql",
        "mongodb",
        "sqlite",
        "oracle",
        "sql server",
    ],
}


def extract_skills(
    text: str,
    custom_skills: Iterable[str] | None = None,
) -> list[str]:
    """Extract recognized technical skills from text."""

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    if not text.strip():
        return []

    skills = {
        skill
        for category_skills in SKILL_DATABASE.values()
        for skill in category_skills
    }

    if custom_skills:
        skills.update(
            skill.strip().lower()
            for skill in custom_skills
            if isinstance(skill, str) and skill.strip()
        )

    text_lower = text.lower()
    found_skills = []

    for skill in skills:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(found_skills)


def extract_skills_by_category(text: str) -> dict[str, list[str]]:
    """Extract recognized skills grouped by category."""

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    text_lower = text.lower()
    results = {}

    for category, skills in SKILL_DATABASE.items():
        found = []

        for skill in skills:
            pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

            if re.search(pattern, text_lower):
                found.append(skill)

        results[category] = sorted(found)

    return results
