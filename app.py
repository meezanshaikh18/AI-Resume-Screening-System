import os
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from src.resume_parser import parse_resume
from src.job_description_parser import parse_job_description
from src.candidate_ranker import rank_candidates
from src.report_generator import generate_csv_report

st.set_page_config(
    page_title="HireAI | Resume Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
REPORT_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_PATH = REPORT_DIR / "candidate_ranking_report.csv"

PAPER = "#F5F0E7"
INK = "#20211D"
BURNT = "#C45B35"
OLIVE = "#777B54"
SAND = "#D8CCB9"
WHITE = "#FFFFFF"

DEFAULTS = {
    "job_profile": None,
    "candidate_profiles": [],
    "ranked_candidates": [],
    "analysis_complete": False,
    "job_description_saved": "",
    "last_processed_count": 0,
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

css_path = ASSETS_DIR / "style.css"
custom_css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""

st.markdown("""
<style>
:root {
 --paper:#F5F0E7; --ink:#20211D; --burnt:#C45B35;
 --olive:#777B54; --sand:#D8CCB9; --white:#FFFFFF;
}
.stApp {background:var(--paper);color:var(--ink)}
[data-testid="stHeader"] {background:rgba(245,240,231,.92)}
[data-testid="stSidebar"] {background:var(--ink);border-right:1px solid rgba(216,204,185,.25)}
[data-testid="stSidebar"] * {color:var(--paper)}
[data-testid="stSidebar"] [data-testid="stRadio"] label {padding:.55rem .7rem;border-radius:9px}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {background:rgba(245,240,231,.1)}
.main .block-container {max-width:1450px;padding-top:2.1rem;padding-bottom:3rem}
h1,h2,h3 {color:var(--ink)!important;letter-spacing:-.035em}
.brand-kicker {color:var(--burnt);font-size:.72rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase}
.page-title {font-size:2.05rem;font-weight:800;margin:.2rem 0 .35rem}
.page-subtitle {color:#66665D;font-size:.96rem;margin-bottom:1.4rem}
.metric-card {background:var(--white);border:1px solid var(--sand);border-radius:15px;padding:1.05rem 1.15rem;min-height:128px}
.metric-label {color:#77766D;font-size:.78rem;font-weight:650}
.metric-value {color:var(--ink);font-size:1.85rem;font-weight:800;margin-top:.45rem}
.metric-note {color:var(--olive);font-size:.75rem;margin-top:.15rem}
.candidate-card,.panel {background:var(--white);border:1px solid var(--sand);border-radius:14px;padding:1rem 1.1rem}
.score-pill {display:inline-block;background:#F3E5DC;color:var(--burnt);border-radius:20px;padding:.25rem .65rem;font-weight:800}
.small-muted {color:#77766D;font-size:.82rem}
div.stButton>button[kind="primary"],button[kind="primary"] {background:var(--burnt);border:1px solid var(--burnt);color:white;border-radius:9px;font-weight:700}
div.stButton>button[kind="primary"]:hover {background:#A94B2C;border-color:#A94B2C;color:white}
.stTextArea textarea,.stTextInput input {background:white;border-color:var(--sand);border-radius:10px}
[data-testid="stFileUploader"] {background:white;border:1px dashed var(--sand);border-radius:12px;padding:.5rem}
hr {border-color:var(--sand)}
footer {visibility:hidden}
</style>
""", unsafe_allow_html=True)
if custom_css:
    st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)


def page_heading(kicker, title, subtitle):
    st.markdown(
        f'<div class="brand-kicker">{kicker}</div>'
        f'<div class="page-title">{title}</div>'
        f'<div class="page-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )


def metric_card(label, value, note):
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


def ranking_dataframe(candidates):
    rows = []
    for item in candidates:
        score = item.get("overall_score")
        rows.append({
            "Rank": item.get("rank") if item.get("rank") is not None else "—",
            "Candidate": item.get("file_name", "Unknown"),
            "Match Score": f"{score:.2f}%" if score is not None else "N/A",
            "Status": item.get("status", "unknown").replace("_", " ").title(),
        })
    return pd.DataFrame(rows)


def process_resumes(job_description, uploaded_resumes):
    job_profile = parse_job_description(job_description)
    candidate_profiles, failures = [], []
    progress = st.progress(0, text="Preparing resume analysis...")

    for index, resume in enumerate(uploaded_resumes):
        temp_path = None
        try:
            suffix = Path(resume.name).suffix.lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(resume.getvalue())
                temp_path = temp_file.name
            candidate = parse_resume(temp_path)
            candidate["file_name"] = resume.name
            candidate_profiles.append(candidate)
        except Exception as exc:
            failures.append((resume.name, str(exc)))
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
        progress.progress((index + 1) / len(uploaded_resumes),
                          text=f"Processed {index + 1} of {len(uploaded_resumes)} resumes")

    progress.empty()
    if not candidate_profiles:
        raise RuntimeError("No resumes could be processed successfully.")

    ranked = rank_candidates(candidate_profiles, job_profile)
    st.session_state["job_profile"] = job_profile
    st.session_state["candidate_profiles"] = candidate_profiles
    st.session_state["ranked_candidates"] = ranked
    st.session_state["analysis_complete"] = True
    st.session_state["job_description_saved"] = job_description
    st.session_state["last_processed_count"] = len(candidate_profiles)

    generate_csv_report(ranked, str(REPORT_PATH),
                        job_profile.get("job_title") or "Untitled Position")
    return failures


def show_candidate_details(candidate):
    components = candidate.get("component_scores", {})
    score = candidate.get("overall_score")

    # Overall match score
    if score is not None:
        st.metric("Overall match score", f"{score:.2f}%")
    else:
        st.warning(
            "Insufficient information to calculate a match score."
        )

    # Skills evaluation
    skills = components.get("skills")

    if isinstance(skills, dict):
        st.markdown("#### Skills evaluation")

        skills_score = skills.get("score")
        if isinstance(skills_score, (int, float)):
            st.progress(max(0.0, min(1.0, skills_score / 100)))
            st.write(f"**Skills match:** {skills_score:.2f}%")
        else:
            st.info("Skills match score is unavailable.")

        left, right = st.columns(2)

        with left:
            st.markdown("**Matched required skills**")
            st.write(
                ", ".join(skills.get("matched_skills", []))
                or "None identified"
            )

        with right:
            st.markdown("**Missing required skills**")
            st.write(
                ", ".join(skills.get("missing_skills", []))
                or "None identified"
            )

    # Numeric evaluation criteria
    st.markdown("#### Other evaluation criteria")

    labels = {
        "text_similarity": "Job description text similarity",
        "experience": "Experience match",
    }

    shown = False

    for key, label in labels.items():
        value = components.get(key)

        if isinstance(value, (int, float)):
            shown = True
            st.write(f"**{label}:** {value:.2f}%")

    # Structured education evaluation
    education = components.get("education")

    if isinstance(education, dict):
        shown = True
        st.markdown("#### Education evaluation")

        education_score = education.get("score")

        if isinstance(education_score, (int, float)):
            st.write(f"**Education match:** {education_score:.2f}%")
            st.progress(
                max(0.0, min(1.0, education_score / 100))
            )
        else:
            st.info(
                "Education match could not be calculated because "
                "sufficient evidence was unavailable."
            )

        status = education.get("status", "not_available")
        st.write(
            f"**Evaluation status:** "
            f"{str(status).replace('_', ' ').title()}"
        )

        degree_match = education.get("degree_level_match")
        if degree_match is not None:
            st.write(
                "**Degree-level match:** "
                + ("Yes" if degree_match else "No")
            )

        field_match = education.get("field_match")
        if field_match is not None:
            st.write(
                "**Field-of-study match:** "
                + ("Yes" if field_match else "No")
            )

        with st.expander("View education matching details"):
            st.markdown("**Matched degree levels**")
            st.write(
                ", ".join(education.get("matched_levels", []))
                or "None identified"
            )

            st.markdown("**Exact field matches**")
            st.write(
                ", ".join(education.get("exact_field_matches", []))
                or "None identified"
            )

            st.markdown("**Related field matches**")
            related_matches = education.get("related_field_matches", [])

            if related_matches:
                for item in related_matches:
                    st.write(
                        f"- {item.get('candidate_field', 'Unknown')} "
                        f"→ {item.get('required_field', 'Unknown')}"
                    )
            else:
                st.write("None identified")

            st.markdown("**Missing required fields**")
            st.write(
                ", ".join(education.get("missing_fields", []))
                or "None"
            )

            st.markdown("**Explanation**")
            st.write(
                education.get(
                    "explanation",
                    "No explanation available."
                )
            )

    elif isinstance(education, (int, float)):
        # Backward compatibility with older numeric results.
        shown = True
        st.write(f"**Education match:** {education:.2f}%")

    if not shown:
        st.caption(
            "No additional evaluation components were available."
        )

    st.caption(
        "Automated estimates require recruiter verification."
    )

# Sidebar navigation
with st.sidebar:
    st.markdown(
        f'<div style="padding:.7rem .3rem 1.5rem">'
        f'<div style="font-size:1.65rem;font-weight:850;letter-spacing:-.05em;color:{PAPER}">'
        f'Hire<span style="color:{BURNT}">AI</span></div>'
        f'<div style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;'
        f'color:{SAND};margin-top:.2rem">Resume Intelligence</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div style="font-size:.68rem;color:{SAND};font-weight:800;letter-spacing:.14em;margin:0 0 .55rem .45rem">WORKSPACE</div>',
                unsafe_allow_html=True)
    page = st.radio(
        "Main navigation",
        ["Dashboard", "Analyze Resumes", "Candidates", "Analytics", "Reports", "Settings"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Recruiter workspace · Human-led hiring decisions")


# Dashboard
if page == "Dashboard":
    page_heading("Recruiter workspace", "Dashboard",
                 "A clear overview of screening activity and candidate matches.")
    ranked = st.session_state["ranked_candidates"]
    profiles = st.session_state["candidate_profiles"]
    job = st.session_state["job_profile"]
    scored = [x for x in ranked if x.get("overall_score") is not None]
    scores = [x["overall_score"] for x in scored]

    cols = st.columns(4)
    values = [
        ("TOTAL CANDIDATES", str(len(profiles)), "Successfully processed resumes"),
        ("JOBS ANALYZED", str(1 if job else 0), "Job descriptions evaluated"),
        ("AVERAGE MATCH", f"{sum(scores)/len(scores):.1f}%" if scores else "—", "Across candidates with scores"),
        ("TOP MATCH", f"{max(scores):.1f}%" if scores else "—", "Highest calculated match"),
    ]
    for col, (label, value, note) in zip(cols, values):
        with col:
            metric_card(label, value, note)

    st.write("")
    left, right = st.columns([1.65, 1])
    with left:
        st.markdown("### Recent candidate matches")
        if ranked:
            st.dataframe(ranking_dataframe(ranked), width="stretch", hide_index=True)
            st.caption("Rankings reflect the criteria available for each candidate.")
        else:
            st.markdown('<div class="panel"><b>No candidate analysis yet</b><br><span class="small-muted">Add a job description and upload resumes to begin.</span></div>',
                        unsafe_allow_html=True)
    with right:
        st.markdown("### Current job")
        if job:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown(f"**{job.get('job_title') or 'Untitled position'}**")
            st.write(f"Required skills: {len(job.get('skills', {}).get('required_skills', []))}")
            st.write(f"Preferred skills: {len(job.get('skills', {}).get('preferred_skills', []))}")
            exp = job.get("minimum_experience_years")
            st.write(f"Minimum experience: {exp if exp is not None else 'Not specified'}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="panel"><span class="small-muted">No job description analyzed yet.</span></div>',
                        unsafe_allow_html=True)
        st.write("")
        st.button("＋  Analyze new resumes", type="primary", width="stretch",
                  on_click=lambda: st.session_state.update({"nav_target": "Analyze Resumes"}))
    if ranked:
        st.write("")
        st.markdown("### Top candidate")
        top = next((x for x in ranked if x.get("overall_score") is not None), None)
        if top:
            st.markdown('<div class="candidate-card">', unsafe_allow_html=True)
            a, b, c = st.columns([2, 1, 1])
            with a:
                st.markdown(f"**{top.get('file_name', 'Unknown')}**")
                st.caption("Highest calculated match in this analysis")
            with b:
                st.markdown(f'<span class="score-pill">{top["overall_score"]:.2f}% match</span>',
                            unsafe_allow_html=True)
            with c:
                st.caption(f"Rank #{top.get('rank')}")
            st.markdown("</div>", unsafe_allow_html=True)


# Analyze resumes
elif page == "Analyze Resumes":
    page_heading("Screening workflow", "Analyze resumes",
                 "Add a job description, upload candidate documents, and calculate match scores.")
    with st.form("resume_analysis_form"):
        st.markdown("### 01 · Job description")
        jd = st.text_area(
            "Paste the complete job description",
            value=st.session_state.get("job_description_saved", ""),
            height=230,
            placeholder="Job Title: Python Developer\n\nRequired Skills:\n- Python\n- Machine Learning\n- SQL\n\nMinimum 3 years of experience.",
        )
        st.markdown("### 02 · Candidate resumes")
        uploads = st.file_uploader("Upload PDF or DOCX resumes",
                                   type=["pdf", "docx"], accept_multiple_files=True)
        submitted = st.form_submit_button("Analyze candidates", type="primary",
                                          width="stretch")

    if uploads:
        st.caption(f"{len(uploads)} file(s) selected.")
    if submitted:
        if not jd.strip():
            st.error("Please provide a job description.")
        elif not uploads:
            st.error("Please upload at least one PDF or DOCX resume.")
        else:
            try:
                with st.spinner("Extracting requirements, parsing resumes and calculating matches..."):
                    failures = process_resumes(jd, uploads)
                st.success(f"Analysis complete. {st.session_state['last_processed_count']} candidate(s) processed and ranked.")
                for filename, message in failures:
                    st.warning(f"{filename} could not be processed: {message}")
                job = st.session_state["job_profile"]
                st.markdown("### Job requirement summary")
                a, b = st.columns(2)
                with a:
                    st.write(f"**Job title:** {job.get('job_title') or 'Not detected'}")
                    st.write(f"**Minimum experience:** {job.get('minimum_experience_years') if job.get('minimum_experience_years') is not None else 'Not specified'}")
                with b:
                    st.write("**Required skills:** " + (", ".join(job["skills"]["required_skills"]) or "None detected"))
                    st.write("**Preferred skills:** " + (", ".join(job["skills"]["preferred_skills"]) or "None detected"))
                st.markdown("### Candidate ranking")
                st.dataframe(ranking_dataframe(st.session_state["ranked_candidates"]),
                             width="stretch", hide_index=True)
                st.info("Open Candidates to inspect each candidate's detailed evaluation.")
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")

    if st.session_state["analysis_complete"]:
        st.divider()
        st.caption(f"Latest analysis: {len(st.session_state['candidate_profiles'])} candidate(s) processed.")


# Candidates
elif page == "Candidates":
    page_heading("Candidate directory", "Candidates",
                 "Review extracted evidence and inspect the scoring breakdown.")
    ranked = st.session_state["ranked_candidates"]
    profiles = {x.get("file_name"): x for x in st.session_state["candidate_profiles"]}
    if not ranked:
        st.info("No candidates available yet. Go to Analyze Resumes to start.")
    else:
        st.dataframe(ranking_dataframe(ranked), width="stretch", hide_index=True)
        st.divider()
        for candidate in ranked:
            name = candidate.get("file_name", "Unknown")
            score = candidate.get("overall_score")
            title = (f"#{candidate.get('rank')} · {name} · {score:.2f}%"
                     if score is not None else f"{name} · Insufficient data")
            with st.expander(title):
                details, evaluation = st.columns([1.4, 1])
                profile = profiles.get(name, {})
                with details:
                    st.markdown("#### Extracted profile")
                    st.write("**Recognized skills**")
                    st.write(", ".join(profile.get("skills", [])) or "No recognized skills found.")
                    st.write("**Skills by category**")
                    st.json(profile.get("skills_by_category", {}))
                    st.write("**Experience details**")
                    st.json(profile.get("experience", {}))
                    st.write("**Education details**")
                    st.json(profile.get("education", {}))
                with evaluation:
                    st.markdown("#### Evaluation")
                    show_candidate_details(candidate)


# Analytics
elif page == "Analytics":
    page_heading("Screening insights", "Analytics",
                 "Explore the distribution of calculated candidate match scores.")
    scored = [x for x in st.session_state["ranked_candidates"]
              if x.get("overall_score") is not None]
    if not scored:
        st.info("Run a candidate analysis to populate analytics.")
    else:
        frame = pd.DataFrame([
            {"Candidate": x.get("file_name", "Unknown"), "Match score": x["overall_score"]}
            for x in scored
        ])
        a, b, c = st.columns(3)
        for col, label, value, note in [
            (a, "AVERAGE MATCH", f"{frame['Match score'].mean():.2f}%", "Mean calculated score"),
            (b, "HIGHEST MATCH", f"{frame['Match score'].max():.2f}%", "Highest calculated score"),
            (c, "LOWEST MATCH", f"{frame['Match score'].min():.2f}%", "Lowest calculated score"),
        ]:
            with col:
                metric_card(label, value, note)
        st.write("")
        st.markdown("### Candidate score comparison")
        st.bar_chart(frame.set_index("Candidate"), y="Match score")
        st.caption("Scores are outputs of the current weighted method, not probabilities of job performance.")


# Reports
elif page == "Reports":
    page_heading("Export center", "Reports",
                 "Download the latest candidate ranking report for recruiter review.")
    ranked = st.session_state["ranked_candidates"]
    if not ranked:
        st.info("No report is available yet. Analyze resumes first.")
    else:
        job = st.session_state["job_profile"]
        st.markdown("### Latest ranking report")
        st.write(f"**Position:** {job.get('job_title') or 'Untitled position'}")
        st.write(f"**Candidates:** {len(ranked)}")
        if not REPORT_PATH.exists():
            generate_csv_report(ranked, str(REPORT_PATH),
                                job.get("job_title") or "Untitled Position")
        st.download_button("Download candidate ranking report (CSV)",
                           data=REPORT_PATH.read_bytes(),
                           file_name="candidate_ranking_report.csv",
                           mime="text/csv", type="primary", width="stretch")
        st.markdown("### Report preview")
        st.dataframe(ranking_dataframe(ranked), width="stretch", hide_index=True)


# Settings
elif page == "Settings":
    page_heading("Workspace preferences", "Settings",
                 "Review the current evaluation configuration and application information.")
    st.markdown("### Current scoring weights")
    for label, value in [
        ("Required skills", "40%"),
        ("Job description text similarity", "30%"),
        ("Experience", "20%"),
        ("Education", "10%"),
    ]:
        st.write(f"**{label}:** {value}")
    st.warning(
        "These are provisional engineering weights, not scientifically validated "
        "predictors of job performance. Review and validate them before consequential use."
    )
    st.markdown("### About HireAI")
    st.write("HireAI extracts resume information, compares candidate evidence with job requirements, "
             "and presents decision-support scores.")
    st.markdown("### Privacy and responsible use")
    st.write("Use only candidate information you are authorized to process. Do not use protected "
             "or sensitive personal attributes in scoring. Recruiters must verify evidence and make "
             "all hiring decisions.")


st.divider()
st.caption(
    "HireAI · AI-assisted recruiter decision support · Scores are estimates, not probabilities. "
    "Final hiring decisions must remain human-led."
)
