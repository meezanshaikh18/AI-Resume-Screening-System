
from pathlib import Path

import pymupdf
from docx import Document


RESUME_DIR = Path("data/sample_data")
RESUME_DIR.mkdir(parents=True, exist_ok=True)

sample_text = """
ALEX JOHNSON

Python Developer

PROFESSIONAL SUMMARY
Python developer with 3 years of experience in software development
and machine learning.

TECHNICAL SKILLS
Python, SQL, Machine Learning, Pandas, NumPy, Scikit-learn

WORK EXPERIENCE
Python Developer - ABC Technologies
January 2023 - Present

EDUCATION
Bachelor of Computer Science
"""


# Generate sample PDF
pdf_path = RESUME_DIR / "sample_resume.pdf"

pdf = pymupdf.open()
page = pdf.new_page()
page.insert_textbox(
    pymupdf.Rect(50, 50, 550, 750),
    sample_text,
    fontsize=11,
)
pdf.save(pdf_path)
pdf.close()


# Generate sample DOCX
docx_path = RESUME_DIR / "sample_resume.docx"

document = Document()
document.add_heading("ALEX JOHNSON", level=1)

for line in sample_text.splitlines():
    if line.strip() and line != "ALEX JOHNSON":
        document.add_paragraph(line)

document.save(docx_path)

print("Sample PDF and DOCX resumes created successfully!")
print(f"PDF: {pdf_path}")
print(f"DOCX: {docx_path}")
