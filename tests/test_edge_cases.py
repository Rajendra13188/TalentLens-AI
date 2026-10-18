"""
Additional edge-case and boundary tests for TalentLens AI.
Covers empty JDs, special characters, zero-match resumes, and custom weights.
"""

import pytest
from src.matcher import ResumeMatcher
from src.data_models import ExtractionResult, ExtractionStatus
from src.skills_extractor import SkillsExtractor


def test_empty_job_description_handling():
    matcher = ResumeMatcher()
    ext = ExtractionResult(
        filename="resume1.pdf",
        status=ExtractionStatus.SUCCESS,
        clean_text="Python Machine Learning Docker"
    )
    # When JD is empty string, should not crash, returns candidate results with score 0 or baseline
    results = matcher.screen_candidates("", [ext])
    assert len(results) == 1
    assert results[0].overall_score == 0.0


def test_zero_matching_skills_resume():
    matcher = ResumeMatcher()
    jd = "Required: Python, PyTorch, Scikit-Learn, Deep Learning"
    ext = ExtractionResult(
        filename="culinary_resume.pdf",
        status=ExtractionStatus.SUCCESS,
        clean_text="Executive chef with 10 years experience in French cuisine, knife skills, and kitchen management."
    )
    results = matcher.screen_candidates(jd, [ext])
    assert len(results) == 1
    # Skill match should be 0
    assert results[0].score_breakdown.skill_match_score == 0.0
    assert len(results[0].matched_skills) == 0
    assert len(results[0].missing_skills) == 4
    assert results[0].overall_score <= 10.0


def test_special_characters_in_jd():
    matcher = ResumeMatcher()
    jd = "Role: C++ & C# developer with CI/CD @ high-frequency trading firm! $$$ %%% &&& ***"
    ext = ExtractionResult(
        filename="dev.pdf",
        status=ExtractionStatus.SUCCESS,
        clean_text="Expert C++ developer with CI/CD experience."
    )
    results = matcher.screen_candidates(jd, [ext])
    assert len(results) == 1
    assert "C++" in results[0].matched_skills
    assert "CI/CD" in results[0].matched_skills


def test_dynamic_weight_adjustment():
    matcher = ResumeMatcher(weight_tfidf=0.8, weight_skills=0.2, weight_breadth=0.0)
    matcher.update_weights(weight_tfidf=0.2, weight_skills=0.7, weight_breadth=0.1)
    assert matcher.weight_tfidf == 0.2
    assert matcher.weight_skills == 0.7
    assert matcher.weight_breadth == 0.1


def test_candidate_tier_property():
    res_high = ExtractionResult(filename="high.pdf", status=ExtractionStatus.SUCCESS, clean_text="Test")
    matcher = ResumeMatcher()
    scored_high = matcher.screen_candidates("Python", [res_high])[0]
    scored_high.overall_score = 82.0
    assert scored_high.tier == "Strong Match"

    scored_high.overall_score = 60.0
    assert scored_high.tier == "Moderate Match"

    scored_high.overall_score = 35.0
    assert scored_high.tier == "Partial Match"

    scored_high.overall_score = 15.0
    assert scored_high.tier == "Low Alignment"
