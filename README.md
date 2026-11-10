# HireAI — AI Resume Screening & Candidate Ranking System

HireAI is a Python and Streamlit-based resume screening application that extracts structured information from PDF and DOCX resumes, compares candidate profiles with a job description, and presents explainable candidate match scores to support recruiter review.

> **Important:** HireAI is a decision-support project, not an automated hiring system. Its extracted information and match scores can be incomplete or inaccurate. A qualified human reviewer must assess candidates using job-related criteria. Do not use the score as the sole basis for hiring or rejection.

## Overview

Reviewing many resumes manually can be time-consuming. HireAI streamlines parts of the initial review process by:

- Extracting text from PDF and DOCX resumes.
- Cleaning and preprocessing resume text.
- Identifying skills and grouping them by category.
- Extracting experience and education information.
- Parsing job descriptions for role, skills, experience, and education requirements.
- Comparing candidate profiles against job requirements.
- Ranking candidates using configurable, weighted matching criteria.
- Displaying candidate analysis and reports through a Streamlit interface.

## Key Features

- **PDF and DOCX parsing:** Reads text from supported resume formats.
- **Resume information extraction:** Builds candidate profiles containing skills, experience, and education details.
- **Job description parsing:** Identifies job title, required/preferred skills, minimum experience, and education requirements.
- **Skill matching:** Compares extracted candidate skills with required job skills and identifies matched and missing skills.
- **Text similarity:** Uses TF-IDF vectorization and cosine similarity to estimate similarity between resume text and the job description.
- **Experience matching:** Compares extracted experience with the minimum experience requirement.
- **Education matching:** Evaluates available qualification and field-of-study information.
- **Candidate ranking:** Sorts candidates by calculated match score and keeps candidates with insufficient information unscored.
- **Interactive interface:** Provides Dashboard, Analyze Resumes, Candidates, Analytics, Reports, and Settings sections.
- **CSV reporting:** Generates a candidate ranking report.
- **Automated tests:** Includes pytest tests for the processing, extraction, matching, scoring, ranking, and reporting modules.

## Candidate Matching & Score Weights

HireAI's default scoring configuration uses four criteria:

| Matching criterion | Default weight |
|---|---:|
| Skills match | 40% |
| Job description text similarity | 30% |
| Experience match | 20% |
| Education match | 10% |
| **Total** | **100%** |

The weights are defined in `src/scoring_engine.py` and can be overridden when calling the scoring and ranking functions.

### How the criteria are calculated

- **Skills match:** Measures the proportion of required skills found in the candidate's extracted skills.
- **Text similarity:** Uses TF-IDF with unigrams and bigrams, followed by cosine similarity, to compare processed resume text with the job description.
- **Experience match:** Compares the candidate's extracted experience with the job's minimum experience requirement, capped at 100% when the requirement is met or exceeded.
- **Education match:** Uses the project's education-matching logic to evaluate available qualification and field-of-study information.

**Missing evidence is not automatically treated as a zero score.** A criterion is included only when the information needed to evaluate it is available. The active weights are then normalized to calculate the overall score. If no criterion can be evaluated, the candidate receives an `insufficient_data` status and no overall score.

These are configurable matching heuristics, not a validated measure of candidate quality or future job performance.

## Technology Stack

| Area | Technologies |
|---|---|
| Language | Python |
| User interface | Streamlit |
| Data handling | Pandas, NumPy |
| NLP and text processing | spaCy, regular expressions |
| Similarity and matching | Scikit-learn (TF-IDF, cosine similarity) |
| PDF processing | PyMuPDF |
| DOCX processing | python-docx |
| Fuzzy matching | RapidFuzz |
| Visualizations | Plotly |
| Testing | pytest |

Dependency requirements are listed in [`requirements.txt`](requirements.txt).

## Project Structure

```text
AI-Resume-Screening-System/
│
├── app.py                         # Streamlit application
├── requirements.txt               # Project dependencies
├── README.md                      # Project documentation
├── .gitignore                     # Ignored files and local data
│
├── .streamlit/
│   └── config.toml                # Streamlit configuration
│
├── assets/
│   └── style.css                  # Application styling
│
├── data/
│   ├── sample_data/               # Sample PDF and DOCX resumes
│   └── processed/                 # Generated reports (ignored by Git)
│
├── src/
│   ├── candidate_ranker.py        # Candidate sorting and ranking
│   ├── document_processor.py      # PDF and DOCX text extraction
│   ├── education_extractor.py     # Education extraction
│   ├── experience_extractor.py    # Experience extraction
│   ├── job_description_parser.py  # Job requirement parsing
│   ├── matching_engine.py         # Skills, text, experience, education matching
│   ├── report_generator.py        # Candidate report generation
│   ├── resume_parser.py           # Resume-to-profile processing pipeline
│   ├── scoring_engine.py          # Weighted candidate scoring
│   ├── skill_extractor.py         # Skill extraction and categorization
│   └── text_preprocessor.py       # Text cleaning and preprocessing
│
└── tests/
    ├── create_sample_resumes.py   # Generate sample resume files
    └── test_*.py                  # Automated tests for project modules
```

## Requirements

- Python installed on your system.
- `pip` for installing Python packages.
- Git to clone the repository.
- A terminal such as PowerShell, Command Prompt, or a Unix shell.

Use a Python version compatible with the packages in `requirements.txt`.

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/meezanshaikh18/AI-Resume-Screening-System.git
cd AI-Resume-Screening-System
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation in the current terminal session, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If the application reports that the spaCy English model is missing, install it with:

```bash
python -m spacy download en_core_web_sm
```

## Run the Application

From the project root, with the virtual environment activated, run:

```bash
python -m streamlit run app.py
```

Streamlit will display a local address in the terminal, usually `http://localhost:8501`. Open that address in your browser.

To stop the application, press `Ctrl + C` in the terminal.

## Generate Sample Resumes

The repository includes a helper script that generates sample resume files for local testing:

```bash
python tests/create_sample_resumes.py
```

Use synthetic/sample documents when testing. Do not add real candidate resumes or personal information to the repository.

## Run Tests

Run the automated test suite from the project root:

```bash
python -m pytest tests/ -v
```

The tests cover candidate profiles, document extraction and processing, resume parsing, job-description parsing, skill/experience/education extraction, matching, scoring, ranking, and report generation.

## Data & Privacy

Resumes can contain sensitive personal information. Follow these precautions:

- Use synthetic resumes for development, testing, and demonstrations.
- Do not commit real resumes, candidate names, contact details, or other personally identifiable information.
- Do not commit passwords, API keys, access tokens, `.env` files, or Streamlit secrets.
- Review generated reports before sharing them. The `data/processed/` directory is excluded from version control by the repository's `.gitignore`.
- For any real-world use, apply appropriate authorization, consent, access controls, secure storage, and data-retention practices.
- Review extracted information and matching results for errors, missing context, and potential bias.

## Troubleshooting

### `streamlit` is not recognized

Ensure the virtual environment is activated and dependencies are installed. You can launch Streamlit through Python:

```bash
python -m streamlit run app.py
```

### A Python package is missing

Reinstall the project dependencies in the active environment:

```bash
python -m pip install -r requirements.txt
```

### spaCy language model is missing

Install the English model:

```bash
python -m spacy download en_core_web_sm
```

### Tests are not discovered

Run pytest from the repository root:

```bash
python -m pytest tests/ -v
```

## Potential Future Improvements

- Improve parsing for resumes with complex layouts, tables, and scanned pages.
- Expand and maintain skill dictionaries and configurable skill categories.
- Add more transparent explanations for each matching criterion.
- Expand tests for unusual document formats and extraction edge cases.
- Add secure, access-controlled storage and audit trails for authorized deployments.

## Contributing

Suggestions and contributions are welcome:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and add or update relevant tests.
4. Run the test suite.
5. Open a pull request describing your changes.

## Disclaimer

HireAI is an educational and decision-support project. Resume parsing, information extraction, and candidate matching may be incomplete, inaccurate, or affected by the quality and format of the supplied documents. Match scores are heuristic estimates, not objective measures of candidate ability. Do not use automated scores or rankings as the sole basis for hiring, rejection, or other employment decisions. Keep a human decision-maker involved and evaluate candidates fairly using relevant job criteria and applicable privacy and employment requirements.

## Acknowledgements

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Scikit-learn](https://scikit-learn.org/)
- [spaCy](https://spacy.io/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [Plotly](https://plotly.com/python/)

## Connect With Me

I'm always open to connecting with fellow developers, collaborating on interesting projects, and exploring opportunities in AI/ML.

- **GitHub:** [GitHub Profile](https://github.com/meezanshaikh18)
- **LinkedIn:** [LinkedIn Profile](https://www.linkedin.com/in/meezanshaikh18/)
- **Portfolio:** [Portfolio Website](https://meezan-shaikh-portfolio-meezan-shaikhs-projects-081392b8.vercel.app/)

If you find this project interesting, consider giving the repository a ⭐ star!
