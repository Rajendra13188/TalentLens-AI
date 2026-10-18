"""
Generate professional 10-slide presentation for TalentLens AI college project submission.
Uses python-pptx to generate TalentLens_AI_Presentation.pptx in submission_docs.
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = Path(__file__).resolve().parent.parent
SUBMISSION_DIR = BASE_DIR / "submission_docs"
IMAGES_DIR = SUBMISSION_DIR / "images"
PPTX_OUT = SUBMISSION_DIR / "TalentLens_AI_Presentation.pptx"

# Theme Colors
COLOR_NAVY = RGBColor(30, 58, 138)       # #1E3A8A Primary Dark
COLOR_BLUE = RGBColor(37, 99, 235)       # #2563EB Accent Blue
COLOR_DARK = RGBColor(31, 41, 55)        # #1F2937 Text Dark
COLOR_MUTED = RGBColor(107, 114, 128)    # #6B7280 Muted Gray
COLOR_LIGHT = RGBColor(248, 250, 252)    # #F8FAFC Background Light
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_AMBER = RGBColor(180, 83, 9)       # #B45309 Placeholder Highlight
COLOR_GREEN = RGBColor(4, 120, 87)       # #047857 Success Green


def set_slide_background(slide, color):
    """Sets background fill of a slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header(slide, title_text, category_text="TALENTLENS AI — AI RESUME SCREENING SYSTEM"):
    """Adds a standard header banner to a content slide."""
    # Top Category Pill / Label
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.4), Inches(0.35))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_BLUE

    # Slide Main Title
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY
    p_title.space_after = Pt(10)


def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(10.0)
    prs.slide_height = Inches(5.625)  # 16:9 Widescreen aspect ratio
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, COLOR_NAVY)

    # Accent decorative bar
    bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.12), Inches(2.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_BLUE
    bar.line.fill.background()

    # Title box
    t_box = slide1.shapes.add_textbox(Inches(1.1), Inches(1.0), Inches(8.2), Inches(3.4))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p1 = tf1.paragraphs[0]
    p1.text = "TalentLens AI"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    p2 = tf1.add_paragraph()
    p2.text = "AI Resume Screening System — College Capstone Project"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(191, 219, 254)  # Light blue
    p2.space_after = Pt(16)

    p3 = tf1.add_paragraph()
    p3.text = "Author: [STUDENT_NAME] (Roll No: [ROLL_NUMBER])"
    p3.font.size = Pt(13)
    p3.font.color.rgb = COLOR_WHITE

    p4 = tf1.add_paragraph()
    p4.text = "Supervisor: [SUPERVISOR_NAME] • [DEPARTMENT_NAME], [COLLEGE_NAME]"
    p4.font.size = Pt(12)
    p4.font.color.rgb = RGBColor(229, 231, 235)

    p5 = tf1.add_paragraph()
    p5.text = "Repository: https://github.com/Rajendra13188/TalentLens-AI"
    p5.font.size = Pt(11)
    p5.font.color.rgb = RGBColor(254, 215, 170)  # Light amber highlight

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, COLOR_LIGHT)
    add_header(slide2, "Problem Statement & Industry Motivation")

    # Content boxes (2 columns)
    # Left Column: The Problem
    box_left = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(4.0), Inches(3.6))
    box_left.fill.solid()
    box_left.fill.fore_color.rgb = COLOR_WHITE
    box_left.line.color.rgb = RGBColor(229, 231, 235)
    tf_l = box_left.text_frame
    tf_l.word_wrap = True
    p_lt = tf_l.paragraphs[0]
    p_lt.text = "The Modern Hiring Dilemma"
    p_lt.font.size = Pt(15)
    p_lt.font.bold = True
    p_lt.font.color.rgb = COLOR_NAVY
    p_lt.space_after = Pt(10)

    points_l = [
        "Mass Application Overload: Recruiters receive hundreds of resumes per technical job opening.",
        "ATS 'Black-Box' Syndrome: Legacy tools output opaque percentages without explainable justifications.",
        "Privacy & Compliance Risks: Cloud screening APIs expose confidential applicant PII to external vendors.",
        "Brittle Document Parsers: Systems crash on corrupted, blank, or scanned PDFs."
    ]
    for pt in points_l:
        p = tf_l.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # Right Column: The Solution
    box_right = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.1), Inches(1.4), Inches(4.1), Inches(3.6))
    box_right.fill.solid()
    box_right.fill.fore_color.rgb = RGBColor(239, 246, 255)
    box_right.line.color.rgb = COLOR_BLUE
    tf_r = box_right.text_frame
    tf_r.word_wrap = True
    p_rt = tf_r.paragraphs[0]
    p_rt.text = "The TalentLens AI Approach"
    p_rt.font.size = Pt(15)
    p_rt.font.bold = True
    p_rt.font.color.rgb = COLOR_BLUE
    p_rt.space_after = Pt(10)

    points_r = [
        "100% Free & Local Execution: Completely sovereign offline screening without paid APIs or API keys.",
        "Transparent Mathematical Scoring: Explainable 0–100 matching formula displayed per candidate.",
        "Zero-Retention In-Memory Storage: Uploaded resumes parsed in-memory and never saved to disk.",
        "Fault-Tolerant PyMuPDF Extractor: Detects and isolates corrupt, empty, and scanned image documents."
    ]
    for pt in points_r:
        p = tf_r.add_paragraph()
        p.text = f"✔ {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_DARK
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 3: PROJECT OBJECTIVES & ARCHITECTURE
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, COLOR_LIGHT)
    add_header(slide3, "System Architecture & Processing Pipeline")

    arch_img = IMAGES_DIR / "architecture_diagram.png"
    if arch_img.exists():
        slide3.shapes.add_picture(str(arch_img), Inches(0.8), Inches(1.35), Inches(8.4), Inches(3.8))

    # =========================================================================
    # SLIDE 4: TECHNOLOGY STACK & CORE MODULES
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, COLOR_LIGHT)
    add_header(slide4, "Technology Stack & Core Engineering Modules")

    stack_items = [
        ("Streamlit (1.65.0)", "Interactive Web UI", "Provides reactive dashboard, preset selectors, candidate deep-dive inspectors, and skill-gap charts."),
        ("PyMuPDF (1.28.2)", "PDF Document Extractor", "C-backed high performance extraction; catches corrupt files and identifies scanned/blank documents."),
        ("scikit-learn (1.9.1)", "TF-IDF Vectorization", "Unigram & bigram TF-IDF vectorizer with sublinear scaling; computes angular cosine similarity."),
        ("pandas & numpy", "Data Analytics & CSV", "Structures candidate leaderboards, rank percentiles, pool skill-gap aggregations, and export CSVs."),
        ("Custom Regex Engine", "Skills Taxonomy", "Symbol-aware lookarounds for C++, C#, .NET, CI/CD; handles contextual aliases (import pandas as pd)."),
        ("pytest (9.1.1)", "Automated QA Suite", "Automated test suite (30/30 passing) verifying extractors, scoring logic, edge cases, and UI flow.")
    ]

    for idx, (lib, role, desc) in enumerate(stack_items):
        col = idx % 3
        row = idx // 3
        x = Inches(0.8 + col * 2.85)
        y = Inches(1.4 + row * 1.85)

        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(2.7), Inches(1.7))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_WHITE
        card.line.color.rgb = RGBColor(229, 231, 235)

        ctf = card.text_frame
        ctf.word_wrap = True
        p_lib = ctf.paragraphs[0]
        p_lib.text = lib
        p_lib.font.size = Pt(13)
        p_lib.font.bold = True
        p_lib.font.color.rgb = COLOR_NAVY

        p_role = ctf.add_paragraph()
        p_role.text = role
        p_role.font.size = Pt(10)
        p_role.font.bold = True
        p_role.font.color.rgb = COLOR_BLUE
        p_role.space_after = Pt(4)

        p_desc = ctf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(9.5)
        p_desc.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 5: EXPLAINABLE SCORING FORMULA
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, COLOR_LIGHT)
    add_header(slide5, "Explainable Scoring Engine & Formulation")

    # Formula Card Banner
    f_card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.35), Inches(8.4), Inches(1.1))
    f_card.fill.solid()
    f_card.fill.fore_color.rgb = COLOR_NAVY
    f_card.line.fill.background()

    f_tf = f_card.text_frame
    f_tf.word_wrap = True
    pf1 = f_tf.paragraphs[0]
    pf1.text = "Deterministic Overall Score Formula (0 to 100):"
    pf1.font.size = Pt(11)
    pf1.font.color.rgb = RGBColor(191, 219, 254)

    pf2 = f_tf.add_paragraph()
    pf2.text = "Final Score = (w_skills × S_skills) + (w_tfidf × S_tfidf) + (w_breadth × B_breadth)"
    pf2.font.size = Pt(17)
    pf2.font.bold = True
    pf2.font.color.rgb = COLOR_WHITE

    # 3 Component Breakdowns
    components = [
        ("JD Skill Coverage (S_skills)", "Weight: 40% (0.40)", "Proportion of required skills in JD matched by resume:\nS_skills = (|Skills_JD ∩ Skills_Resume| / |Skills_JD|) × 100", "#10B981"),
        ("TF-IDF Cosine Similarity (S_tfidf)", "Weight: 50% (0.50)", "Sublinear TF-IDF unigram/bigram cosine angle:\nS_tfidf = cos(v_JD, v_Resume) × 100.0\nIdentifies top overlapping terms.", "#F59E0B"),
        ("Domain Breadth Bonus (B_breadth)", "Weight: 10% (0.10)", "Rewards relevant complementary skills outside JD:\nB_breadth = min(10.0, |Skills_Resume \\ Skills_JD| × 1.5)", "#8B5CF6")
    ]
    for idx, (name, wt, desc, col_hex) in enumerate(components):
        x = Inches(0.8 + idx * 2.85)
        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.6), Inches(2.7), Inches(2.5))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_WHITE
        card.line.color.rgb = RGBColor(229, 231, 235)

        ctf = card.text_frame
        ctf.word_wrap = True
        pn = ctf.paragraphs[0]
        pn.text = name
        pn.font.size = Pt(12)
        pn.font.bold = True
        pn.font.color.rgb = COLOR_DARK

        pw = ctf.add_paragraph()
        pw.text = wt
        pw.font.size = Pt(11)
        pw.font.bold = True
        pw.font.color.rgb = COLOR_BLUE
        pw.space_after = Pt(8)

        pd = ctf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 6: DOCUMENT INGESTION & ROBUSTNESS
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, COLOR_LIGHT)
    add_header(slide6, "Fault-Tolerant Document Ingestion & Edge Cases")

    cases = [
        ("Scanned / Image-Only PDFs", "Detected when page contains images but extracted digital characters < 40.", "Action: Classified as 'Scanned / Image-Only PDF', alerts recruiter that OCR is needed. System does NOT crash.", COLOR_AMBER),
        ("Empty / Blank PDFs", "Detected when file is 0 bytes or document contains zero digital text.", "Action: Assigned score 0.0 with explicit status 'Empty / Blank PDF', documented in summary banner.", COLOR_BLUE),
        ("Corrupted Binary Streams", "Malformed PDF headers or truncated trailers caught via PyMuPDF FileDataError.", "Action: Trapped gracefully, flagged as 'Corrupted or Invalid PDF', isolated at the bottom of rankings.", COLOR_NAVY),
        ("In-Memory Privacy Guarantee", "Resumes processed via memory bytes (BytesIO).", "Action: Zero disk persistence. Documents exist only in active browser RAM session and are discarded immediately.", COLOR_GREEN),
    ]

    for idx, (title, detect, action, color) in enumerate(cases):
        row = idx // 2
        col = idx % 2
        x = Inches(0.8 + col * 4.3)
        y = Inches(1.4 + row * 1.85)

        box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(4.1), Inches(1.7))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_WHITE
        box.line.color.rgb = color
        box.line.width = Pt(1.5)

        btf = box.text_frame
        btf.word_wrap = True
        pt = btf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = color

        pd = btf.add_paragraph()
        pd.text = f"• Condition: {detect}"
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_DARK
        pd.space_after = Pt(2)

        pa = btf.add_paragraph()
        pa.text = f"• Handling: {action}"
        pa.font.size = Pt(9.5)
        pa.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 7: EXPERIMENTAL MULTI-ROLE EVALUATION
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, COLOR_LIGHT)
    add_header(slide7, "Experimental Results — Dynamic Multi-Role Screening")

    chart_img = IMAGES_DIR / "role_comparison_chart.png"
    if chart_img.exists():
        slide7.shapes.add_picture(str(chart_img), Inches(0.8), Inches(1.35), Inches(8.4), Inches(3.8))

    # =========================================================================
    # SLIDE 8: COMPREHENSIVE AUTOMATED TESTING (30 TESTS)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, COLOR_LIGHT)
    add_header(slide8, "Quality Assurance & Automated Pytest Suite")

    test_img = IMAGES_DIR / "test_results_summary.png"
    if test_img.exists():
        slide8.shapes.add_picture(str(test_img), Inches(0.8), Inches(1.35), Inches(8.4), Inches(3.8))

    # =========================================================================
    # SLIDE 9: ETHICAL AI & FAIR HIRING FRAMEWORK
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, COLOR_LIGHT)
    add_header(slide9, "Ethical AI Governance & Fair Hiring Framework")

    ethics = [
        ("1. TF-IDF Is Not Human Competency", "TF-IDF measures vocabulary and keyword frequency overlap. It is strictly a textual alignment indicator and NOT a probabilistic prediction of candidate on-the-job success, intelligence, or cultural fit."),
        ("2. Absence of Keyword ≠ Absence of Capability", "The dashboard explicitly labels unlocated skills as 'Skill Not Detected' rather than 'Candidate Lacks Skill', clarifying that keywords may simply be expressed differently or omitted."),
        ("3. Demographic Neutrality", "TalentLens AI completely excludes all protected demographic characteristics (gender, age, ethnicity, religion, disability, photo) from extraction and scoring algorithms."),
        ("4. Zero-Retention Data Privacy", "Candidate resumes are processed entirely in memory during active sessions without persistent saving to local disks or transmission to third-party cloud servers.")
    ]

    for idx, (head, desc) in enumerate(ethics):
        y = Inches(1.35 + idx * 0.95)
        bar = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(8.4), Inches(0.85))
        bar.fill.solid()
        bar.fill.fore_color.rgb = COLOR_WHITE
        bar.line.color.rgb = RGBColor(229, 231, 235)

        btf = bar.text_frame
        btf.word_wrap = True
        ph = btf.paragraphs[0]
        ph.text = head
        ph.font.size = Pt(12)
        ph.font.bold = True
        ph.font.color.rgb = COLOR_NAVY

        pd = btf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 10: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, COLOR_NAVY)

    c_box = slide10.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(8.0), Inches(4.0))
    ctf = c_box.text_frame
    ctf.word_wrap = True

    p_ct = ctf.paragraphs[0]
    p_ct.text = "Conclusion & Future Roadmap"
    p_ct.font.size = Pt(26)
    p_ct.font.bold = True
    p_ct.font.color.rgb = COLOR_WHITE
    p_ct.space_after = Pt(14)

    concl_points = [
        "Delivered a complete, sovereign, explainable AI Resume Screening System using local Python libraries.",
        "Replaced black-box neural scoring with transparent 0–100 mathematical breakdowns displayed in real-time.",
        "Achieved 100% test pass rate across 30 automated unit, integration, and UI acceptance tests.",
        "Future Scope: Integration of local offline OCR (Tesseract) for scanned paper archives.",
        "Future Scope: Lightweight offline semantic embeddings (e.g., all-MiniLM-L6-v2) to complement TF-IDF.",
        "Future Scope: Experience duration parsing to automatically quantify years of experience per technology."
    ]
    for pt in concl_points:
        p = ctf.add_paragraph()
        p.text = f"✔ {pt}"
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(229, 231, 235)
        p.space_after = Pt(6)

    prs.save(str(PPTX_OUT))
    print(f"Successfully generated presentation at: {PPTX_OUT}")


if __name__ == "__main__":
    create_presentation()
