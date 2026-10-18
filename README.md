# 🎯 TalentLens AI — AI Resume Screening System

> **College Capstone Project**  
> An explainable, local AI-powered resume screening system built with **Python**, **Streamlit**, **scikit-learn**, **PyMuPDF**, and **pandas**.  
> **GitHub Repository:** [https://github.com/Rajendra13188/TalentLens-AI](https://github.com/Rajendra13188/TalentLens-AI)

---

## 📌 Executive Summary & Problem Statement

Modern recruitment pipelines process hundreds of resumes per job posting. Traditional Applicant Tracking Systems (ATS) often operate as opaque "black boxes" or rely on expensive, non-private cloud APIs that compromise applicant data. Furthermore, naive keyword filters often reject qualified applicants without transparency.

**TalentLens AI** is an explainable, privacy-preserving, local AI resume screening system designed to solve these challenges:
- **100% Free & Local Execution:** Runs completely offline on local machines without paid external APIs, API keys, or cloud transfers.
- **Explainable Scoring (0–100):** Every candidate's score is mathematically transparent, combining TF-IDF cosine similarity, direct job skill coverage, and domain breadth bonuses.
- **Robust Document Ingestion:** Uses PyMuPDF to extract text from digital PDFs while gracefully detecting corrupted, blank, and scanned image PDFs without crashing.
- **Ethical AI & Fair Hiring:** Strictly evaluates technical alignment and excludes all protected personal demographics (gender, race, age, religion).

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3.13** | Core programming language |
| **Streamlit** | Interactive web dashboard and UI |
| **scikit-learn** | TF-IDF vectorization and cosine similarity computation |
| **PyMuPDF (`pymupdf`)** | High-performance digital PDF text extraction and document inspection |
| **pandas & numpy** | Structured data manipulation, analytics, and CSV exports |
| **pytest** | Automated test suite covering edge cases and pipeline integration |

---

## 📋 System Architecture & Workflow

```
                        ┌────────────────────────────────────────┐
                        │        Job Description (Text)          │
                        └───────────────────┬────────────────────┘
                                            │
┌─────────────────────────┐                 │
│ Candidate PDF Resumes   │                 │
│ (Uploaded / Demo Data)  │                 │
└───────────┬─────────────┘                 │
            │                               │
            ▼                               │
┌─────────────────────────┐                 │
│     PyMuPDF Extractor   │                 │
│  - Corrupt PDF Catch    │                 │
│  - Empty PDF Catch      │                 │
│  - Scanned Image Catch  │                 │
└───────────┬─────────────┘                 │
            │ Clean Text                    │
            ├───────────────────────────────┤
            ▼                               ▼
┌─────────────────────────┐   ┌───────────────────────────┐
│ Configurable Skills     │   │   TF-IDF Vectorizer &     │
│ Extraction Engine       │   │   Cosine Similarity       │
│ (7 Taxonomy Domains)    │   │   (Unigram & Bigram Model)│
└───────────┬─────────────┘   └─────────────┬─────────────┘
            │                               │
            │ Overlap & Gaps                │ Cosine Score [0, 1]
            └───────────────┬───────────────┘
                            ▼
              ┌───────────────────────────┐
              │ Explainable Scoring (0-100│
              │ Formula: W_skill + W_tfidf│
              └─────────────┬─────────────┘
                            ▼
              ┌───────────────────────────┐
              │ Streamlit UI Dashboard    │
              │  - Leaderboard Ranking    │
              │  - Candidate Deep Dive    │
              │  - Skill Gap Analytics    │
              │  - CSV Export             │
              └───────────────────────────┘
```

---

## 🧮 Explainable Scoring Engine

Rather than relying on uninterpretable neural embeddings, TalentLens AI calculates candidate alignment using an exact, transparent formula:

$$\text{Final Score} = \min\left(100.0, \; \left(w_{\text{skills}} \times S_{\text{skills}}\right) + \left(w_{\text{tfidf}} \times S_{\text{tfidf}}\right) + \left(w_{\text{breadth}} \times B_{\text{breadth}}\right)\right)$$

### Default Weight Configuration:
- **$w_{\text{skills}} = 0.40$ (40%):** Direct Job Description Skill Coverage.
- **$w_{\text{tfidf}} = 0.50$ (50%):** Vocabulary & Contextual TF-IDF Cosine Similarity.
- **$w_{\text{breadth}} = 0.10$ (10%):** Domain Breadth Bonus for relevant complementary technical skills.

### Component Details:
1. **$S_{\text{skills}}$ (Skill Coverage %):**
   $$\frac{|\text{Skills}_{\text{JD}} \cap \text{Skills}_{\text{Resume}}|}{|\text{Skills}_{\text{JD}}|} \times 100$$
2. **$S_{\text{tfidf}}$ (TF-IDF Cosine Similarity %):**
   $$\cos(\mathbf{v}_{\text{JD}}, \mathbf{v}_{\text{Resume}}) \times 100$$
3. **$B_{\text{breadth}}$ (Breadth Bonus Points):**
   $$\min(10.0, |\text{Skills}_{\text{Resume}} \setminus \text{Skills}_{\text{JD}}| \times 1.5)$$

---

## 🛡️ Ethical AI & Transparency Principles

1. **TF-IDF Scores Are Not Probabilities of Job Success:**  
   TF-IDF measures linguistic and keyword overlap between documents. A high score means strong textual alignment with the posted description, but does not predict on-the-job human capability or culture fit.
2. **"Skill Not Detected" Does Not Mean Lacking Capability:**  
   If a skill is listed as "Not Detected", it only indicates that the specific keyword or its configured aliases were not present in the extracted text.
3. **Demographic Neutrality:**  
   No protected demographic characteristics (gender, race, age, religion, nationality, disability) are parsed, extracted, or included in scoring calculations.
4. **Zero-Retention In-Memory Processing:**  
   Uploaded PDF files are parsed directly in memory (`BytesIO`). Files are not saved to disk or transmitted to any third-party server.

---

## 📁 Project Structure

```
TalentLens AI/
├── app.py                      # Main Streamlit web application
├── requirements.txt            # Python dependencies
├── README.md                   # Comprehensive project documentation
├── .gitignore                  # Git ignore rules
├── src/
│   ├── __init__.py             # Package marker
│   ├── config.py               # Weights, taxonomy, and disclaimers
│   ├── data_models.py          # Data classes & extraction enums
│   ├── pdf_extractor.py        # PyMuPDF extraction & edge-case handler
│   ├── skills_extractor.py     # Regex-based configurable skills engine
│   └── matcher.py              # TF-IDF, cosine similarity, & scoring engine
├── sample_data/
│   ├── sample_jobs.json        # Pre-configured job descriptions
│   ├── generate_sample_pdfs.py # Synthetic demo PDF generation script
│   └── resumes/                # 7 Synthetic demo resumes (valid + edge cases)
│       ├── candidate_01_aisha_sharma_senior_ml.pdf
│       ├── candidate_02_david_chen_data_analyst.pdf
│       ├── candidate_03_elena_rodriguez_fullstack_dev.pdf
│       ├── candidate_04_marcus_vance_cloud_devops.pdf
│       ├── candidate_05_scanned_image_sample.pdf
│       ├── candidate_06_empty_sample.pdf
│       └── candidate_07_corrupted_sample.pdf
└── tests/
    ├── __init__.py
    ├── test_pdf_extractor.py   # PDF extraction & error handling tests
    ├── test_skills_extractor.py# Skills detection & alias matching tests
    ├── test_matcher.py         # TF-IDF, formula, and ranking tests
    ├── test_edge_cases.py      # Edge case & boundary condition tests
    └── test_end_to_end.py      # End-to-end batch screening test
```

---

## 🚀 Installation & Running Guide

### Step 1: Clone or Navigate to the Project Directory

```powershell
git clone https://github.com/Rajendra13188/TalentLens-AI.git
cd TalentLens-AI
```

### Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 3: Run Automated Tests

Execute all 24 unit and integration tests to verify system integrity:
```powershell
pytest -v
```

### Step 4: Launch the Streamlit Application

```powershell
streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501`.

---

## 🧪 Test Results & Verification

All automated tests execute and pass cleanly:
```
============================= test session starts =============================
platform win32 -- Python 3.13.16, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\pedam\Downloads\UG Research
collected 24 items

tests/test_edge_cases.py::test_empty_job_description_handling PASSED     [  4%]
tests/test_edge_cases.py::test_zero_matching_skills_resume PASSED        [  8%]
tests/test_edge_cases.py::test_special_characters_in_jd PASSED           [ 12%]
tests/test_edge_cases.py::test_dynamic_weight_adjustment PASSED          [ 16%]
tests/test_edge_cases.py::test_candidate_tier_property PASSED            [ 20%]
tests/test_end_to_end.py::test_end_to_end_screening_pipeline PASSED      [ 25%]
tests/test_matcher.py::test_tfidf_identical_texts PASSED                 [ 29%]
tests/test_matcher.py::test_score_calculation_bounds_and_formula PASSED  [ 33%]
tests/test_matcher.py::test_top_overlapping_terms PASSED                 [ 37%]
tests/test_matcher.py::test_candidate_ranking_order PASSED               [ 41%]
tests/test_pdf_extractor.py::test_clean_text_normalizes_whitespace PASSED [ 45%]
tests/test_pdf_extractor.py::test_clean_text_handles_control_chars PASSED [ 50%]
tests/test_pdf_extractor.py::test_extract_valid_pdf PASSED               [ 54%]
tests/test_pdf_extractor.py::test_extract_scanned_image_pdf PASSED       [ 58%]
tests/test_pdf_extractor.py::test_extract_empty_pdf PASSED               [ 62%]
tests/test_pdf_extractor.py::test_extract_corrupted_pdf PASSED           [ 66%]
tests/test_pdf_extractor.py::test_extract_from_empty_bytes PASSED        [ 70%]
tests/test_pdf_extractor.py::test_extract_from_invalid_bytes PASSED      [ 75%]
tests/test_skills_extractor.py::test_extract_basic_skills PASSED         [ 79%]
tests/test_skills_extractor.py::test_extract_tricky_symbols PASSED       [ 83%]
tests/test_skills_extractor.py::test_extract_multi_word_phrases PASSED   [ 87%]
tests/test_skills_extractor.py::test_extract_cloud_and_devops PASSED     [ 91%]
tests/test_skills_extractor.py::test_compare_skills PASSED               [ 95%]
tests/test_skills_extractor.py::test_add_custom_skill PASSED             [100%]

============================= 24 passed in 2.07s ==============================
```

---

## 🎯 Verification with Synthetic Demo Resumes

The application includes 7 built-in synthetic test documents demonstrating system capabilities:
1. **`candidate_01_aisha_sharma_senior_ml.pdf`**: Senior ML Engineer profile (High match for ML/AI role).
2. **`candidate_02_david_chen_data_analyst.pdf`**: Data Analyst profile (Moderate match for ML, high match for BI).
3. **`candidate_03_elena_rodriguez_fullstack_dev.pdf`**: React/Node.js Fullstack profile (Low match for ML, high for Web).
4. **`candidate_04_marcus_vance_cloud_devops.pdf`**: AWS/Kubernetes DevOps profile.
5. **`candidate_05_scanned_image_sample.pdf`**: Image-only PDF with zero text characters (Correctly flagged as `Scanned / Image-Only PDF`, OCR required).
6. **`candidate_06_empty_sample.pdf`**: Zero-byte/blank PDF (Correctly flagged as `Empty / Blank PDF`).
7. **`candidate_07_corrupted_sample.pdf`**: Truncated/malformed binary file (Correctly flagged as `Corrupted or Invalid PDF`).
