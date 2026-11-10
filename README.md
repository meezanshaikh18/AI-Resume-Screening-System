# AI Resume Screening & Candidate Ranking System

An AI-assisted resume screening application that extracts information
from PDF and DOCX resumes, processes candidate text, identifies relevant
skills, and helps compare and rank applicants against job requirements
through an interactive Streamlit interface.

> **Project status:** This repository is being prepared for its initial
> public release. Review the configuration and sample data before
> publishing. Do not upload real candidate resumes, personally
> identifiable information, credentials, or confidential recruitment
> data.

## Overview

Manually reviewing a large number of resumes can be time-consuming. This
project streamlines parts of that workflow by:

-   Reading resume files in **PDF** and **DOCX** formats.
-   Extracting and cleaning resume text.
-   Processing text with **spaCy lemmatization**.
-   Identifying skills using curated regular-expression patterns.
-   Organizing extracted skills into categories and supporting custom
    skills.
-   Supporting candidate comparison and ranking for a job requirement.
-   Providing a Streamlit-based interface for interacting with the
    workflow.

The system is intended to assist recruiters and developers with resume
analysis. Its output should be treated as decision-support information,
not as an automated hiring decision.

## Key Features

-   **Resume parsing:** Extract text from PDF and Word documents.
-   **Text preprocessing:** Clean and normalize extracted resume
    content.
-   **Lemmatization:** Process text using spaCy.
-   **Skill extraction:** Detect skills with curated regex patterns.
-   **Categorized skills:** Return skills grouped by category, alongside
    extracted skills.
-   **Candidate ranking:** Compare candidate profiles with job
    requirements and display ranking results.
-   **Streamlit UI:** Use the application through a browser-based
    interface.
-   **Tests:** Run the project's automated test suite with pytest.

## Technology Stack

  Area                          Technology
  ----------------------------- ---------------------
  Programming language          Python
  User interface                Streamlit
  Natural language processing   spaCy
  Text processing               Python
  Skill extraction              Regular expressions
  Document formats              PDF, DOCX
  Automated testing             pytest

The exact package versions are maintained in
[`requirements.txt`](requirements.txt).

## Project Structure

``` text
AI-Resume-Screening-System/
│
├── app.py                         # Streamlit application entry point
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── .gitignore                     # Files excluded from Git
│
├── .streamlit/
│   └── config.toml                # Streamlit theme configuration
│
├── assets/
│   └── style.css                  # Application styling
│
├── data/
│   ├── sample_data/               # Synthetic/sample resumes for testing
│   └── processed/                 # Generated output (excluded from Git)
│
├── src/                           # Application and processing modules
│
└── tests/
    ├── create_sample_resumes.py   # Generates sample resumes
    └── ...                        # Automated tests
```

Some directories may contain additional modules or files as the project
evolves. Generated reports and local cache files should remain outside
version control.

## Requirements

-   Python installed on your system.
-   pip, Python's package installer.
-   Git, if cloning the repository.
-   A terminal such as PowerShell, Command Prompt, or a Unix shell.

Use a Python version supported by the packages pinned in
`requirements.txt`.

## Installation

### 1. Clone the repository

``` bash
git clone https://github.com/meezanshaikh18/AI-Resume-Screening-System.git
cd AI-Resume-Screening-System
```

### 2. Create a virtual environment

**Windows PowerShell:**

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current terminal session, run:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Upgrade pip and install dependencies

``` bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If the project reports that a spaCy language model is missing, install
the English model used by the application:

``` bash
python -m spacy download en_core_web_sm
```

## Run the Application

From the project root, with the virtual environment activated:

``` bash
streamlit run app.py
```

Streamlit will print a local URL in the terminal (typically
`http://localhost:8501`). Open that address in your browser.

To stop the application, press `Ctrl + C` in the terminal.

## Generate Sample Resumes

The project includes a helper script for generating sample resumes in
`data/sample_data/`.

``` bash
python tests/create_sample_resumes.py
```

Use generated or otherwise synthetic resumes when testing. Do not use
real candidate documents in a public repository or test environment
unless you have the appropriate authorization and safeguards.

## Run Tests

Install the dependencies first, then run:

``` bash
python -m pytest tests/ -v
```

The test suite covers the project's resume-processing and
skill-extraction functionality. Add or update tests when changing
parsing, preprocessing, extraction, or ranking behavior.

## Expected Resume-Processing Output

The resume-processing module returns structured information including
fields such as:

-   `file_name`
-   `file_type`
-   `raw_text`
-   `cleaned_text`
-   `processed_text`
-   `skills`
-   `skills_by_category`

The exact output and ranking details are determined by the current
implementation in `src/`.

## Data, Privacy & Security

Resumes can contain sensitive personal information. Follow these
precautions:

-   Use synthetic resumes for development and demonstrations.
-   Do not commit real resumes, candidate contact details, or personally
    identifiable information.
-   Do not commit `.env` files, API keys, passwords, tokens, or
    Streamlit secrets.
-   Review generated CSV reports before sharing them. The
    `data/processed/` directory is ignored by Git.
-   Store production candidate data securely and apply appropriate
    access controls, retention rules, and consent requirements.
-   Treat extracted skills and ranking results as fallible; review
    candidates fairly and keep a human decision-maker involved.

## Troubleshooting

### `streamlit` is not recognized

Make sure the virtual environment is activated, then run:

``` bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### A Python package is missing

Install the project's dependencies again:

``` bash
python -m pip install -r requirements.txt
```

### spaCy model error

If the application specifically reports that `en_core_web_sm` is
missing, run:

``` bash
python -m spacy download en_core_web_sm
```

### Tests are not discovered

Run pytest from the repository root:

``` bash
python -m pytest tests/ -v
```

## Future Improvements

Potential areas for further development include:

-   More robust resume parsing across different document layouts.
-   Expanded skill dictionaries and configurable skill categories.
-   Transparent, explainable candidate-matching criteria.
-   Additional test coverage for ranking and edge cases.
-   Secure persistence and audit trails for authorized deployments.

## Contributing

Contributions and suggestions are welcome.

1.  Fork the repository.
2.  Create a feature branch.
3.  Make your changes and add relevant tests.
4.  Run the test suite.
5.  Open a pull request describing the changes.

## Disclaimer

This project is for educational, development, and decision-support
purposes. Resume parsing and skill matching may be incomplete or
inaccurate. Do not use automated scores or rankings as the sole basis
for hiring, rejection, or other employment decisions. Evaluate
candidates using job-related criteria, human review, and applicable
employment and privacy requirements.

## Author

**Meezan Shaikh**

-   GitHub: [@meezanshaikh18](https://github.com/meezanshaikh18)
-   LinkedIn: [Meezan Shaikh](https://www.linkedin.com/in/meezanshaikh18/)
    
