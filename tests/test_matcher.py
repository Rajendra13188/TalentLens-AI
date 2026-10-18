"""
Unit tests for ResumeMatcher.
Verifies TF-IDF similarity, explainable score calculations, bounds,
top overlapping terms, and ranking behavior.
"""

import pytest
from src.matcher import ResumeMatcher
from src.data_models import ExtractionResult, ExtractionStatus


@pytest.fixture
def matcher():
    return ResumeMatcher(weight_tfidf=0.50, weight_skills=0.40, weight_breadth=0.10)


def test_tfidf_identical_texts(matcher):
    text = "Senior Python Machine Learning Engineer specializing in PyTorch and Docker."
    similarities, _, _ = matcher.compute_tfidf_similarity(text, [text])
    assert pytest.approx(similarities[0], 0.01) == 1.0


def test_score_calculation_bounds_and_formula(matcher):
    # Perfect match scenario
    breakdown = matcher.score_candidate(
        tfidf_similarity=1.0,
        skill_comparison={"jd_skills_count": 5, "matched_count": 5, "additional_count": 4}
    )
    assert 0.0 <= breakdown.overall_score <= 100.0
    assert breakdown.tfidf_score == 100.0
    assert breakdown.skill_match_score == 100.0
    assert "×" in breakdown.formula_explanation

    # Zero match scenario
    zero_breakdown = matcher.score_candidate(
        tfidf_similarity=0.0,
        skill_comparison={"jd_skills_count": 5, "matched_count": 0, "additional_count": 0}
    )
    assert zero_breakdown.overall_score == 0.0
    assert zero_breakdown.tfidf_score == 0.0
    assert zero_breakdown.skill_match_score == 0.0


def test_top_overlapping_terms(matcher):
    jd = "Seeking Python engineer with strong Docker and Kubernetes experience."
    res = "Skilled Python developer containerizing services using Docker and Kubernetes."
    
    sim, vectorizer, matrix = matcher.compute_tfidf_similarity(jd, [res])
    top_terms = matcher.get_top_overlapping_terms(vectorizer, matrix[0:1], matrix[1:2])
    
    assert len(top_terms) > 0
    term_words = [t["term"] for t in top_terms]
    assert any("python" in w or "docker" in w or "kubernetes" in w for w in term_words)


def test_candidate_ranking_order(matcher):
    jd = "Required: Python, PyTorch, Machine Learning, Docker"
    
    ext_high = ExtractionResult(
        filename="high_match.pdf",
        status=ExtractionStatus.SUCCESS,
        clean_text="Python expert in PyTorch and Machine Learning with Docker and Git."
    )
    ext_low = ExtractionResult(
        filename="low_match.pdf",
        status=ExtractionStatus.SUCCESS,
        clean_text="Experienced Ruby on Rails and PHP web developer."
    )
    ext_corrupt = ExtractionResult(
        filename="corrupted.pdf",
        status=ExtractionStatus.CORRUPTED_OR_INVALID,
        error_message="Invalid PDF"
    )

    results = matcher.screen_candidates(jd, [ext_low, ext_corrupt, ext_high])
    
    assert len(results) == 3
    # Top ranked should be ext_high
    assert results[0].filename == "high_match.pdf"
    assert results[0].rank == 1
    assert results[0].overall_score > results[1].overall_score

    # Middle should be ext_low
    assert results[1].filename == "low_match.pdf"
    assert results[1].rank == 2

    # Bottom should be ext_corrupt with score 0
    assert results[2].filename == "corrupted.pdf"
    assert results[2].overall_score == 0.0
    assert results[2].rank == 3
