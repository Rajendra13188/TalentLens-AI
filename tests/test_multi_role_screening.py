"""
Test multi-role screening workflow.
Verifies that screening the same candidate resume against multiple distinct job descriptions
produces dynamically updated, role-appropriate matching scores, matched skills,
missing skill lists, and explainable breakdowns.
"""

import json
from pathlib import Path
import pytest

from src.config import SAMPLE_JOBS_FILE
from src.pdf_extractor import PDFExtractor
from src.matcher import ResumeMatcher


@pytest.fixture
def user_resume_extraction():
    resume_path = Path(r"C:\Users\pedam\OneDrive\Documents\Rajendra Prasad Pedamallu_Resume.pdf")
    assert resume_path.exists(), f"Resume not found at {resume_path}"
    return PDFExtractor.extract_from_path(resume_path)


@pytest.fixture
def sample_jobs():
    with open(SAMPLE_JOBS_FILE, "r") as f:
        return json.load(f)


def test_screening_against_senior_ml_role(user_resume_extraction, sample_jobs):
    ml_job = sample_jobs["Senior Machine Learning Engineer"]["description"]
    matcher = ResumeMatcher()
    results = matcher.screen_candidates(ml_job, [user_resume_extraction])
    
    assert len(results) == 1
    res = results[0]
    
    # Assert exact score behavior for Senior ML role
    assert res.overall_score == 9.6
    assert res.score_breakdown.tfidf_score == 3.1
    assert res.score_breakdown.skill_match_score == 17.6
    assert res.score_breakdown.breadth_bonus == 10.0
    
    # Check matched skills (3 skills)
    assert set(res.matched_skills) == {"Git", "Large Language Models", "Python"}
    
    # Check that major ML frameworks are identified as missing
    missing = set(res.missing_skills)
    assert "PyTorch" in missing
    assert "TensorFlow" in missing
    assert "Scikit-Learn" in missing
    assert "Machine Learning" in missing


def test_screening_against_ai_applications_role(user_resume_extraction, sample_jobs):
    ai_job = sample_jobs["AI Applications & Desktop Systems Engineer"]["description"]
    matcher = ResumeMatcher()
    results = matcher.screen_candidates(ai_job, [user_resume_extraction])
    
    assert len(results) == 1
    res = results[0]
    
    # Assert dramatic improvement when evaluated against aligned JD
    assert res.score_breakdown.skill_match_score == 100.0
    assert len(res.missing_skills) == 0
    assert res.overall_score > 40.0
    
    # Check all key skills matched
    expected_matches = {"Python", "FastAPI", "SQLite", "Large Language Models", "Git", "Kotlin", "Java", "JavaScript", "HTML/CSS"}
    for skill in expected_matches:
        assert skill in res.matched_skills


def test_score_and_skills_update_dynamically(user_resume_extraction, sample_jobs):
    matcher = ResumeMatcher()
    
    # Run 1: ML Engineer
    ml_res = matcher.screen_candidates(sample_jobs["Senior Machine Learning Engineer"]["description"], [user_resume_extraction])[0]
    
    # Run 2: AI Desktop / Applications Engineer
    ai_res = matcher.screen_candidates(sample_jobs["AI Applications & Desktop Systems Engineer"]["description"], [user_resume_extraction])[0]
    
    # Run 3: Full Stack Web Developer
    web_res = matcher.screen_candidates(sample_jobs["Full Stack Web Developer"]["description"], [user_resume_extraction])[0]
    
    # Scores must reflect the differing role requirements
    assert ai_res.overall_score > ml_res.overall_score
    assert ai_res.overall_score > web_res.overall_score
    
    # Matched skills count must differ
    assert len(ai_res.matched_skills) > len(ml_res.matched_skills)
    
    # Missing skills must be dynamic
    assert len(ai_res.missing_skills) < len(ml_res.missing_skills)
    assert "PyTorch" in ml_res.missing_skills
    assert "React" in web_res.missing_skills
