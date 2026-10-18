"""
TalentLens AI — AI Resume Screening System
A professional, transparent, and explainable college project for automated resume screening
using PyMuPDF, TF-IDF cosine similarity, and configurable skills taxonomy.
"""

import io
import json
from pathlib import Path
import pandas as pd
import streamlit as st

from src.config import (
    DEFAULT_WEIGHT_TFIDF,
    DEFAULT_WEIGHT_SKILLS,
    DEFAULT_WEIGHT_BREADTH,
    SAMPLE_JOBS_FILE,
    SAMPLE_RESUMES_DIR,
    DEFAULT_SKILLS_TAXONOMY,
    DISCLAIMER_TFIDF,
    DISCLAIMER_SKILL_ABSENCE,
    DISCLAIMER_FAIRNESS,
    DISCLAIMER_PRIVACY,
)
from src.data_models import ExtractionStatus, ExtractionResult
from src.pdf_extractor import PDFExtractor
from src.skills_extractor import SkillsExtractor
from src.matcher import ResumeMatcher


# --- Page Configuration ---
st.set_page_config(
    page_title="TalentLens AI — AI Resume Screening System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px 16px;
        text-align: center;
    }
    .badge-pill {
        display: inline-block;
        padding: 3px 9px;
        font-size: 0.78rem;
        font-weight: 600;
        border-radius: 12px;
        margin: 2px;
    }
    .badge-matched {
        background-color: #DEF7EC;
        color: #03543F;
        border: 1px solid #31C48D;
    }
    .badge-missing {
        background-color: #FEEBC8;
        color: #7B341E;
        border: 1px solid #F6AD55;
    }
    .badge-additional {
        background-color: #EBF5FF;
        color: #1E429F;
        border: 1px solid #76A9FA;
    }
    .status-alert {
        padding: 10px 14px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_sample_jobs() -> dict:
    """Loads pre-configured sample job descriptions."""
    if SAMPLE_JOBS_FILE.exists():
        with open(SAMPLE_JOBS_FILE, "r") as f:
            return json.load(f)
    return {}


# Initialize Session State
if "skills_extractor" not in st.session_state:
    st.session_state.skills_extractor = SkillsExtractor()

if "screening_results" not in st.session_state:
    st.session_state.screening_results = None

if "job_description_input" not in st.session_state:
    st.session_state.job_description_input = ""

if "demo_resumes_loaded" not in st.session_state:
    st.session_state.demo_resumes_loaded = False


# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://api.iconify.design/heroicons:academic-cap-solid.svg?color=%231E3A8A", width=42)
    st.title("TalentLens AI")
    st.caption("College Project: Explainable AI Resume Screening System")
    st.markdown("---")

    st.subheader("⚙️ Scoring Configuration")
    st.markdown("Adjust the weight distribution for candidate scoring:")

    w_skills = st.slider("JD Skills Match Weight", min_value=0.0, max_value=1.0, value=DEFAULT_WEIGHT_SKILLS, step=0.05,
                         help="Weight attributed to direct overlap of required job skills.")
    w_tfidf = st.slider("TF-IDF Content Similarity Weight", min_value=0.0, max_value=1.0, value=DEFAULT_WEIGHT_TFIDF, step=0.05,
                        help="Weight attributed to vocabulary and contextual similarity.")
    w_breadth = st.slider("Domain Breadth Bonus Weight", min_value=0.0, max_value=0.5, value=DEFAULT_WEIGHT_BREADTH, step=0.05,
                          help="Bonus weight for complementary technical skills outside base JD.")

    weight_sum = w_skills + w_tfidf + w_breadth
    if round(weight_sum, 2) != 1.0:
        st.warning(f"⚠️ Total weight sum is {weight_sum:.2f} (Recommended sum: 1.00)")

    st.markdown("---")
    st.subheader("🛡️ Fair Hiring & Privacy")
    with st.expander("Privacy & In-Memory Guarantee", expanded=False):
        st.info(DISCLAIMER_PRIVACY)
    with st.expander("Fairness & Non-Discrimination", expanded=False):
        st.info(DISCLAIMER_FAIRNESS)
    with st.expander("About TF-IDF Scores", expanded=False):
        st.info(DISCLAIMER_TFIDF)
        st.info(DISCLAIMER_SKILL_ABSENCE)

    st.markdown("---")
    st.caption("Built with Python 3.13 • Streamlit • scikit-learn • PyMuPDF")


# --- MAIN HEADER ---
st.markdown('<div class="main-title">🎯 TalentLens AI — AI Resume Screening System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Explainable, local resume screening combining PyMuPDF document extraction, '
    'TF-IDF vector cosine similarity, and configurable skills taxonomy.</div>',
    unsafe_allow_html=True
)

# Mandatory top alert for ethical AI
st.info(
    f"ℹ️ **Ethical AI Notice**: {DISCLAIMER_TFIDF} "
    f"{DISCLAIMER_SKILL_ABSENCE}",
    icon="⚖️"
)

# --- STEP 1: JOB DESCRIPTION INPUT ---
st.markdown("### 1. Job Description Specification")

sample_jobs = load_sample_jobs()
job_options = ["Custom Job Description"] + list(sample_jobs.keys())

col_sel, col_btn = st.columns([3, 1])
with col_sel:
    selected_job_preset = st.selectbox(
        "Choose a sample role or select 'Custom Job Description':",
        options=job_options,
        index=1 if "Senior Machine Learning Engineer" in job_options else 0
    )

with col_btn:
    st.write("")
    st.write("")
    if st.button("📋 Load Preset Text", use_container_width=True):
        if selected_job_preset in sample_jobs:
            st.session_state.job_description_input = sample_jobs[selected_job_preset]["description"]
            st.rerun()

if "last_selected_preset" not in st.session_state:
    st.session_state.last_selected_preset = selected_job_preset

if selected_job_preset != st.session_state.last_selected_preset:
    st.session_state.last_selected_preset = selected_job_preset
    if selected_job_preset in sample_jobs:
        st.session_state.job_description_input = sample_jobs[selected_job_preset]["description"]
    elif selected_job_preset == "Custom Job Description":
        st.session_state.job_description_input = ""

# If initial load and empty, populate with first sample
if not st.session_state.job_description_input and selected_job_preset in sample_jobs:
    st.session_state.job_description_input = sample_jobs[selected_job_preset]["description"]

job_description = st.text_area(
    "Job Description Requirements:",
    value=st.session_state.job_description_input,
    height=140,
    placeholder="Paste full job description, required qualifications, and technical skills here...",
    help="Enter the target position's responsibilities, required programming languages, tools, and experience."
)
st.session_state.job_description_input = job_description

# Show instant preview of skills detected in JD
if job_description.strip():
    jd_skills_detected = st.session_state.skills_extractor.extract_skills_set(job_description)
    if jd_skills_detected:
        st.markdown(
            f"**Detected {len(jd_skills_detected)} Skills in Job Description:** " +
            " ".join([f'<span class="badge-pill badge-matched">{s}</span>' for s in sorted(jd_skills_detected)]),
            unsafe_allow_html=True
        )
    else:
        st.caption("No specific skills from active taxonomy detected in the JD text. Scoring will rely primarily on TF-IDF.")

st.markdown("---")

# --- STEP 2: RESUME UPLOAD & DEMO DATA ---
st.markdown("### 2. Resume Ingestion (PDF Documents)")

col_upload, col_demo = st.columns([2, 1])

with col_upload:
    uploaded_files = st.file_uploader(
        "Upload Candidate Resumes (PDF format only):",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or multiple candidate resume PDFs for batch screening."
    )

with col_demo:
    st.markdown("**Or use Synthetic Demo Dataset:**")
    st.caption("Includes 7 realistic candidate profiles plus scanned, empty, and corrupted test documents.")
    if st.button("🚀 Load 7 Synthetic Demo Resumes", use_container_width=True):
        st.session_state.demo_resumes_loaded = True
        st.success("Loaded 7 synthetic demo files!")

# Determine active files to screen
files_to_process = []
if st.session_state.demo_resumes_loaded and SAMPLE_RESUMES_DIR.exists():
    demo_paths = sorted(list(SAMPLE_RESUMES_DIR.glob("candidate_*.pdf")))
    for p in demo_paths:
        with open(p, "rb") as f:
            files_to_process.append({"name": p.name, "bytes": f.read(), "source": "Synthetic Demo"})

if uploaded_files:
    for uf in uploaded_files:
        files_to_process.append({"name": uf.name, "bytes": uf.read(), "source": "Uploaded File"})

if files_to_process:
    st.markdown(f"**Total Resumes Ready for Screening:** `{len(files_to_process)}`")
else:
    st.info("👆 Please upload PDF resumes above or click **'Load 7 Synthetic Demo Resumes'** to begin.")

# Screen Button
st.markdown("")
screen_action = st.button("🔍 Screen & Rank Candidates", type="primary", use_container_width=True)

# Run Screening Pipeline
if screen_action:
    if not job_description.strip():
        st.error("❌ Please provide a Job Description before screening candidates.")
    elif not files_to_process:
        st.error("❌ Please upload at least one PDF resume or load the synthetic demo data.")
    else:
        progress_bar = st.progress(0, text="Extracting text using PyMuPDF...")
        extractions = []
        
        # 1. Extraction Phase
        total = len(files_to_process)
        for idx, item in enumerate(files_to_process):
            progress_bar.progress((idx + 1) / (total + 1), text=f"Processing {item['name']}...")
            ext = PDFExtractor.extract_from_bytes(item["bytes"], filename=item["name"])
            extractions.append(ext)
        
        # 2. Matching and Scoring Phase
        progress_bar.progress(0.95, text="Computing TF-IDF cosine similarity and skill matches...")
        matcher = ResumeMatcher(
            weight_tfidf=w_tfidf,
            weight_skills=w_skills,
            weight_breadth=w_breadth,
            skills_extractor=st.session_state.skills_extractor
        )
        results = matcher.screen_candidates(job_description, extractions)
        progress_bar.progress(1.0, text="Screening Complete!")
        progress_bar.empty()

        st.session_state.screening_results = results
        st.success(f"✅ Successfully screened and ranked {len(results)} candidate resumes!")


# --- RESULTS DASHBOARD ---
if st.session_state.screening_results:
    results = st.session_state.screening_results
    usable_results = [r for r in results if r.extraction.is_usable]
    unusable_results = [r for r in results if not r.extraction.is_usable]

    st.markdown("---")
    st.subheader("📊 Screening Summary & Key Performance Indicators")

    # KPI Metrics
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.metric("Total Resumes", len(results))
    with kpi2:
        st.metric("Scored Candidates", len(usable_results))
    with kpi3:
        st.metric("Flagged / Unusable", len(unusable_results))
    with kpi4:
        avg_score = round(sum(r.overall_score for r in usable_results) / len(usable_results), 1) if usable_results else 0.0
        st.metric("Average Score", f"{avg_score} / 100")
    with kpi5:
        top_cand = usable_results[0] if usable_results else None
        top_str = f"{top_cand.overall_score} pts" if top_cand else "N/A"
        st.metric("Top Score", top_str)

    # Flagged Documents Banner
    if unusable_results:
        with st.expander(f"⚠️ Flagged Unusable Documents ({len(unusable_results)}) — Action Required", expanded=True):
            st.warning(
                "The following files could not be processed digitally. PyMuPDF extracts machine-readable text "
                "layers; files without text layers, corrupted files, or scanned images require OCR or format correction."
            )
            for ur in unusable_results:
                st.markdown(
                    f"- **`{ur.filename}`**: Status **`{ur.extraction.status.value}`** — *{ur.extraction.error_message}*"
                )

    # TABS FOR DETAILED VIEWS
    tab_rankings, tab_inspect, tab_analytics, tab_skills, tab_transparency = st.tabs([
        "🏆 Candidate Leaderboard",
        "🔍 Candidate Inspector",
        "📈 Analytics & Skill Gaps",
        "📚 Skills Taxonomy",
        "⚖️ Fairness & Methodological Details"
    ])

    # --- TAB 1: LEADERBOARD ---
    with tab_rankings:
        st.markdown("#### Ranked Candidate Leaderboard")
        st.caption("Candidates are ordered by explainable matching score (0 to 100).")

        # Prepare DataFrame for table display
        table_rows = []
        for r in results:
            table_rows.append({
                "Rank": f"#{r.rank}",
                "Candidate File": r.filename,
                "Overall Score": f"{r.overall_score:.1f}",
                "Match Tier": r.tier,
                "TF-IDF Similarity": f"{r.score_breakdown.tfidf_score:.1f}%",
                "Skill Match": f"{r.score_breakdown.skill_match_score:.1f}%",
                "Matched Skills Count": len(r.matched_skills),
                "Missing Skills Count": len(r.missing_skills),
                "Status": r.extraction.status.value
            })
        df_leaderboard = pd.DataFrame(table_rows)
        st.dataframe(df_leaderboard, use_container_width=True, hide_index=True)

        # CSV Export
        csv_data = []
        for r in results:
            csv_data.append({
                "Rank": r.rank,
                "Filename": r.filename,
                "Overall_Score": r.overall_score,
                "Tier": r.tier,
                "TFIDF_Score": r.score_breakdown.tfidf_score,
                "Skill_Match_Score": r.score_breakdown.skill_match_score,
                "Breadth_Bonus": r.score_breakdown.breadth_bonus,
                "Matched_Skills": ", ".join(r.matched_skills),
                "Missing_Skills": ", ".join(r.missing_skills),
                "Additional_Skills": ", ".join(r.additional_skills),
                "Extraction_Status": r.extraction.status.value,
                "Error_Message": r.extraction.error_message or ""
            })
        df_export = pd.DataFrame(csv_data)
        csv_bytes = df_export.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Export Screening Results (CSV)",
            data=csv_bytes,
            file_name="talentlens_screening_results.csv",
            mime="text/csv",
            use_container_width=True
        )

    # --- TAB 2: CANDIDATE INSPECTOR ---
    with tab_inspect:
        st.markdown("#### Individual Candidate Deep Dive")
        candidate_names = [f"#{r.rank} - {r.filename} ({r.overall_score:.1f} pts)" for r in results]
        selected_cand_idx = st.selectbox("Select Candidate to Inspect:", range(len(candidate_names)),
                                         format_func=lambda i: candidate_names[i])
        
        cand = results[selected_cand_idx]

        st.markdown(f"### Candidate: `{cand.filename}`")
        badge_color = "green" if cand.overall_score >= 70 else "blue" if cand.overall_score >= 40 else "orange"
        st.markdown(f"**Assigned Rank:** `#{cand.rank}` &nbsp;&nbsp;|&nbsp;&nbsp; **Match Tier:** `{cand.tier}` &nbsp;&nbsp;|&nbsp;&nbsp; **Overall Score:** `{cand.overall_score:.1f} / 100`")

        # Score Breakdown Card
        st.markdown("##### 🧮 Explainable Score Calculation Breakdown")
        st.code(cand.score_breakdown.formula_explanation, language="text")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("TF-IDF Content Match", f"{cand.score_breakdown.tfidf_score:.1f}%",
                      help=f"Weight: {cand.score_breakdown.weight_tfidf:.2f} → Contribution: {cand.score_breakdown.tfidf_points:.2f} pts")
        with c2:
            st.metric("JD Skill Coverage", f"{cand.score_breakdown.skill_match_score:.1f}%",
                      help=f"Weight: {cand.score_breakdown.weight_skills:.2f} → Contribution: {cand.score_breakdown.skill_points:.2f} pts")
        with c3:
            st.metric("Domain Breadth Bonus", f"{cand.score_breakdown.breadth_bonus:.1f} pts",
                      help=f"Weight: {cand.score_breakdown.weight_breadth:.2f} → Contribution: {cand.score_breakdown.breadth_points:.2f} pts")

        # Skills Details
        st.markdown("##### 🏷️ Skills Breakdown")
        
        # Matched Skills
        st.markdown(f"**✅ Matched Skills ({len(cand.matched_skills)}):**")
        if cand.matched_skills:
            st.markdown(" ".join([f'<span class="badge-pill badge-matched">{s}</span>' for s in cand.matched_skills]), unsafe_allow_html=True)
        else:
            st.caption("No matching skills detected between candidate resume and job description.")

        # Skills Not Detected
        st.markdown(f"**⚠️ Skills Not Detected ({len(cand.missing_skills)}):**")
        if cand.missing_skills:
            st.markdown(" ".join([f'<span class="badge-pill badge-missing">{s}</span>' for s in cand.missing_skills]), unsafe_allow_html=True)
            st.caption(f"📌 *Note: {DISCLAIMER_SKILL_ABSENCE}*")
        else:
            st.caption("All skills identified in the job description were detected in this resume.")

        # Additional Skills
        st.markdown(f"**➕ Additional Technical Skills in Resume ({len(cand.additional_skills)}):**")
        if cand.additional_skills:
            st.markdown(" ".join([f'<span class="badge-pill badge-additional">{s}</span>' for s in cand.additional_skills]), unsafe_allow_html=True)
        else:
            st.caption("No additional skills from active taxonomy detected.")

        # Top Overlapping Terms
        if cand.top_overlapping_terms:
            st.markdown("##### 🔍 Top Contributing TF-IDF Terms")
            st.caption("Words and n-grams shared between JD and Resume that contributed most to the similarity score:")
            df_terms = pd.DataFrame(cand.top_overlapping_terms)
            st.dataframe(df_terms, use_container_width=True, hide_index=True)

        # Extracted Text Preview
        with st.expander("📄 View Extracted Text from PDF", expanded=False):
            if cand.extraction.clean_text:
                st.text_area("Extracted Digital Text:", cand.extraction.clean_text, height=220)
            else:
                st.warning(f"No digital text extracted. Reason: {cand.extraction.error_message}")

    # --- TAB 3: ANALYTICS & SKILL GAPS ---
    with tab_analytics:
        st.markdown("#### Applicant Pool Analytics & Skill Gap Insights")
        
        if usable_results:
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.markdown("##### Overall Score Distribution")
                score_data = pd.DataFrame({
                    "Candidate": [r.filename.replace(".pdf", "") for r in usable_results],
                    "Score": [r.overall_score for r in usable_results]
                }).set_index("Candidate")
                st.bar_chart(score_data)

            with chart_col2:
                st.markdown("##### Most Frequent Missing Skills (Talent Gap Analysis)")
                missing_counts = {}
                for r in usable_results:
                    for s in r.missing_skills:
                        missing_counts[s] = missing_counts.get(s, 0) + 1
                if missing_counts:
                    df_missing = pd.DataFrame({
                        "Skill": list(missing_counts.keys()),
                        "Missing Across Candidates": list(missing_counts.values())
                    }).sort_values("Missing Across Candidates", ascending=False).set_index("Skill")
                    st.bar_chart(df_missing)
                else:
                    st.info("No missing skills recorded across applicants.")

            st.markdown("##### Most Common Matched Skills in Pool")
            matched_counts = {}
            for r in usable_results:
                for s in r.matched_skills:
                    matched_counts[s] = matched_counts.get(s, 0) + 1
            if matched_counts:
                df_matched = pd.DataFrame({
                    "Skill": list(matched_counts.keys()),
                    "Candidates Having Skill": list(matched_counts.values())
                }).sort_values("Candidates Having Skill", ascending=False).set_index("Skill")
                st.bar_chart(df_matched)
        else:
            st.info("No usable candidates to display analytics for.")

    # --- TAB 4: SKILLS TAXONOMY ---
    with tab_skills:
        st.markdown("#### Configurable Skills Taxonomy")
        st.caption("Explore or expand the technical skills dictionary used for keyword detection.")

        cat_names = list(st.session_state.skills_extractor.taxonomy.keys())
        sel_cat = st.selectbox("Filter by Skill Category:", cat_names)

        skills_in_cat = st.session_state.skills_extractor.taxonomy[sel_cat]
        tax_rows = []
        for sname, aliases in skills_in_cat.items():
            tax_rows.append({
                "Skill Name": sname,
                "Aliases / Matching Keywords": ", ".join(aliases)
            })
        st.dataframe(pd.DataFrame(tax_rows), use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("##### ➕ Add Custom Skill to Taxonomy")
        with st.form("add_custom_skill_form"):
            new_cat = st.selectbox("Category for New Skill:", cat_names + ["Other / Custom"])
            custom_cat_input = st.text_input("Custom Category Name (if Other selected):", "")
            final_cat = custom_cat_input.strip() if new_cat == "Other / Custom" and custom_cat_input.strip() else new_cat

            new_skill_name = st.text_input("Canonical Skill Name (e.g., 'Rust', 'GraphQL'):")
            new_aliases = st.text_input("Comma-Separated Aliases / Synonyms (e.g., 'rust, rustlang'):")
            
            submit_skill = st.form_submit_button("Add Skill to Dictionary")
            if submit_skill:
                if new_skill_name.strip():
                    alias_list = [a.strip() for a in new_aliases.split(",") if a.strip()]
                    st.session_state.skills_extractor.add_custom_skill(
                        category=final_cat,
                        canonical_name=new_skill_name.strip(),
                        aliases=alias_list
                    )
                    st.success(f"Added skill '{new_skill_name.strip()}' under category '{final_cat}'!")
                    st.rerun()
                else:
                    st.error("Please enter a valid skill name.")

    # --- TAB 5: ETHICS & METHODOLOGY ---
    with tab_transparency:
        st.markdown("#### Ethical AI, Methodology & Limitations")
        st.markdown(f"""
        ### 1. Document Extraction Architecture
        - **Engine:** PyMuPDF (`import pymupdf`).
        - **Handling Edge Cases:** Documents are inspected for font and text streams. If a PDF contains image data but zero or fewer than 40 characters of text, it is classified as a `Scanned / Image-Only PDF` rather than failing silently. Unusable documents receive score 0.0 with clear diagnostic messages.
        
        ### 2. Explainable Scoring Engine
        Candidate scoring avoids opaque neural "black boxes". The score combines three transparent components:
        $$\\text{{Final Score}} = (w_{{\\text{{skills}}}} \\times S_{{\\text{{skills}}}}) + (w_{{\\text{{tfidf}}}} \\times S_{{\\text{{tfidf}}}}) + (w_{{\\text{{breadth}}}} \\times B_{{\\text{{breadth}}}})$$
        
        - **$S_{{\\text{{skills}}}}$ (JD Skill Coverage):** Proportion of skills demanded by the job description detected in the candidate's resume text ($0-100\\%$).
        - **$S_{{\\text{{tfidf}}}}$ (TF-IDF Cosine Similarity):** Sublinear TF-IDF term frequency vector cosine similarity with unigram and bigram representation ($0-100\\%$).
        - **$B_{{\\text{{breadth}}}}$ (Domain Breadth Bonus):** Additional complementary technical skills from the taxonomy present in the candidate profile (up to 10 points).
        
        ### 3. Critical Ethical Principles
        1. **TF-IDF is Not Competency:** {DISCLAIMER_TFIDF}
        2. **Absence of Keyword is Not Absence of Skill:** {DISCLAIMER_SKILL_ABSENCE}
        3. **Fairness & Demographic Neutrality:** {DISCLAIMER_FAIRNESS}
        4. **Privacy:** {DISCLAIMER_PRIVACY}
        """)

else:
    # Empty state illustration
    st.markdown("---")
    st.info("💡 **Ready to screen?** Select a Job Description above, upload candidate PDF resumes or click **'Load 7 Synthetic Demo Resumes'**, and press **'Screen & Rank Candidates'**.")
