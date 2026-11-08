
import os
import tempfile
from pathlib import Path

import streamlit as st

from src.resume_parser import parse_resume
from src.job_description_parser import parse_job_description
from src.candidate_ranker import rank_candidates
from src.report_generator import generate_csv_report


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide",
)


# ==========================================
# CUSTOM STYLING
# ==========================================

css_path = Path(__file__).parent / "assets" / "style.css"

if css_path.exists():
    with open(css_path, encoding="utf-8") as css_file:
        custom_css = css_file.read()

    st.markdown(
        f"<style>{custom_css}</style>",
        unsafe_allow_html=True,
    )


# ==========================================
# APPLICATION HEADER
# ==========================================

st.title("AI Resume Screening & Candidate Ranking System")

st.write(
    "An AI-assisted platform to analyze resumes, "
    "compare candidates against job requirements, "
    "and support recruiter decision-making."
)

st.info(
    "This system provides decision-support scores. "
    "Final hiring decisions must remain with human recruiters."
)


# ==========================================
# 1. JOB DESCRIPTION
# ==========================================

st.divider()
st.header("1. Job Description")

job_description = st.text_area(
    "Paste the job description below",
    height=250,
    placeholder=(
        "Job Title: Python Developer\n\n"
        "Required Skills:\n"
        "- Python\n"
        "- Machine Learning\n"
        "- SQL\n\n"
        "Minimum 2 years of experience."
    ),
    key="job_description",
)

if job_description.strip():
    st.success("Job description added successfully.")
else:
    st.info("Please enter a job description to continue.")


# ==========================================
# 2. UPLOAD CANDIDATE RESUMES
# ==========================================

st.divider()
st.header("2. Upload Candidate Resumes")

uploaded_resumes = st.file_uploader(
    "Upload candidate resumes (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True,
    help="You can upload multiple PDF or DOCX resumes at once.",
)

if uploaded_resumes:
    st.success(
        f"{len(uploaded_resumes)} resume(s) uploaded successfully."
    )

    st.write("### Uploaded Files")

    for resume in uploaded_resumes:
        st.write(f"📄 {resume.name}")

else:
    st.info("Please upload at least one candidate resume.")


# ==========================================
# 3. ANALYZE JOB DESCRIPTION AND RESUMES
# ==========================================

st.divider()
st.header("3. Analyze Job Description & Resumes")

can_analyze = bool(
    job_description.strip() and uploaded_resumes
)

if st.button(
    "Analyze Resumes",
    disabled=not can_analyze,
    type="primary",
    width="stretch",
):

    try:

        # ----------------------------------
        # Parse job description
        # ----------------------------------

        with st.spinner("Analyzing job description..."):
            job_profile = parse_job_description(job_description)

        st.success("Job description analyzed successfully.")

        st.subheader("Job Requirement Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Job Title**")
            st.write(job_profile["job_title"] or "Not detected")

            st.write("**Minimum Experience**")

            minimum_experience = (
                job_profile["minimum_experience_years"]
            )

            if minimum_experience is not None:
                st.write(f"{minimum_experience} years")
            else:
                st.write("Not specified")

        with col2:
            st.write("**Required Skills**")
            st.write(
                job_profile["skills"]["required_skills"] or "None detected"
            )

            st.write("**Preferred Skills**")
            st.write(
                job_profile["skills"]["preferred_skills"] or "None detected"
            )

        st.write("**Education Requirements**")
        st.json(job_profile["education"])

        # ----------------------------------
        # Parse uploaded resumes
        # ----------------------------------

        candidate_profiles = []

        st.divider()
        st.subheader("Candidate Profile Extraction")

        progress_bar = st.progress(0)

        for index, resume in enumerate(uploaded_resumes):

            temp_path = None

            try:

                suffix = Path(resume.name).suffix.lower()

                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix,
                ) as temp_file:

                    temp_file.write(resume.getvalue())
                    temp_path = temp_file.name

                # Parse resume
                candidate = parse_resume(temp_path)

                # Restore original filename
                candidate["file_name"] = resume.name

                candidate_profiles.append(candidate)

                # Display extracted candidate information
                with st.expander(
                    f"Candidate {index + 1}: {resume.name}",
                    expanded=True,
                ):

                    st.write("**Extracted Skills**")
                    st.write(candidate["skills"] or "No recognized skills found.")

                    st.write("**Skills by Category**")
                    st.json(candidate["skills_by_category"])

                    st.write("**Experience Details**")
                    st.json(candidate["experience"])

                    st.write("**Education Details**")
                    st.json(candidate["education"])

                    st.caption(
                        "Extraction results require recruiter verification."
                    )

            except Exception as error:

                st.error(
                    f"Could not process {resume.name}: {error}"
                )

            finally:

                # Delete temporary file
                if temp_path and os.path.exists(temp_path):
                    os.unlink(temp_path)

            progress_bar.progress(
                (index + 1) / len(uploaded_resumes)
            )

        # Save results in session state
        st.session_state["job_profile"] = job_profile
        st.session_state["candidate_profiles"] = candidate_profiles

        st.divider()

        if candidate_profiles:

            st.success(
                f"Successfully processed {len(candidate_profiles)} "
                f"of {len(uploaded_resumes)} resumes."
            )

        else:

            st.error("No resumes could be processed.")

        # ==========================================
        # 4. CANDIDATE RANKING
        # ==========================================

        if candidate_profiles:

            st.divider()
            st.header("4. Candidate Ranking Results")

            with st.spinner("Calculating candidate match scores..."):

                ranked_candidates = rank_candidates(
                    candidate_profiles,
                    job_profile,
                )

            st.session_state["ranked_candidates"] = ranked_candidates

            st.success("Candidate ranking completed successfully.")

            # ----------------------------------
            # Ranking overview
            # ----------------------------------

            st.subheader("Candidate Ranking Overview")

            ranking_rows = []

            for candidate in ranked_candidates:

                score = candidate["overall_score"]

                ranking_rows.append({
                    "Rank": (
                        candidate["rank"]
                        if candidate["rank"] is not None
                        else "N/A"
                    ),
                    "Candidate": candidate["file_name"],
                    "Match Score (%)": (
                        f"{score:.2f}"
                        if score is not None
                        else "N/A"
                    ),
                    "Status": candidate["status"].replace(
                        "_", " "
                    ).title(),
                })

            st.dataframe(
                ranking_rows,
                width="stretch",
                hide_index=True,
            )

            # ----------------------------------
            # Detailed score breakdown
            # ----------------------------------

            st.subheader("Detailed Candidate Evaluation")

            for candidate in ranked_candidates:

                score = candidate["overall_score"]

                if score is not None:
                    expander_title = (
                        f"Rank {candidate['rank']} | "
                        f"{candidate['file_name']} | "
                        f"{score:.2f}%"
                    )
                else:
                    expander_title = (
                        f"{candidate['file_name']} | "
                        "Insufficient Data"
                    )

                with st.expander(expander_title):

                    components = candidate["component_scores"]

                    if candidate["status"] == "insufficient_data":

                        st.warning(
                            "Insufficient information is available "
                            "to calculate a reliable match score."
                        )

                    else:

                        st.metric(
                            "Overall Match Score",
                            f"{score:.2f}%",
                        )

                    # Skills score
                    skills_data = components.get("skills")

                    if isinstance(skills_data, dict):

                        st.write("### Skills Evaluation")

                        skills_score = skills_data.get("score", 0)

                        st.progress(
                            max(0.0, min(1.0, skills_score / 100))
                        )

                        st.write(f"**Skills Match:** {skills_score:.2f}%")

                        st.write(
                            "**Matched Skills:**",
                            ", ".join(
                                skills_data.get("matched_skills", [])
                            ) or "None",
                        )

                        st.write(
                            "**Missing Required Skills:**",
                            ", ".join(
                                skills_data.get("missing_skills", [])
                            ) or "None",
                        )

                    # Other evaluation components
                    component_labels = {
                        "text_similarity": "Job Description Similarity",
                        "experience": "Experience Match",
                        "education": "Education Match",
                    }

                    st.write("### Other Evaluation Criteria")

                    for component_name, label in component_labels.items():

                        value = components.get(component_name)

                        if value is not None:

                            st.write(f"**{label}:** {value:.2f}%")

                    st.caption(
                        "Individual scores are automated estimates. "
                        "Recruiters must verify the extracted information."
                    )

            # ==========================================
            # 5. DOWNLOAD REPORT
            # ==========================================

            st.divider()
            st.header("5. Download Ranking Report")

            report_path = (
                Path(__file__).parent
                / "data"
                / "processed"
                / "candidate_ranking_report.csv"
            )

            generate_csv_report(
                ranked_candidates,
                str(report_path),
                job_profile.get("job_title") or "Untitled Position",
            )

            with open(report_path, "rb") as report_file:

                report_data = report_file.read()

            st.download_button(
                label="Download Candidate Ranking Report (CSV)",
                data=report_data,
                file_name="candidate_ranking_report.csv",
                mime="text/csv",
                type="primary",
                width="stretch",
            )

            st.info(
                "This system is a recruiter decision-support tool. "
                "A match score is not a probability of job success "
                "and must not be used as an automatic hiring or rejection decision."
            )

    except Exception as error:

        st.error(f"Analysis failed: {error}")
