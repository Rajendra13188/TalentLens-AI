"""
End-to-End integration test for TalentLens AI.
Loads the synthetic demo resumes from disk, runs extraction,
screens them against a sample job description, and validates ranking and edge case handling.
"""

import json
import pytest
from pathlib import Path

from src.config import SAMPLE_RESUMES_DIR, SAMPLE_JOBS_FILE
from src.pdf_extractor import PDFExtractor
from src.matcher import ResumeMatcher
from src.data_models import ExtractionStatus


def test_end_to_end_screening_pipeline():
    assert SAMPLE_RESUMES_DIR.exists()
    assert SAMPLE_JOBS_FILE.exists()

    # Load Senior Machine Learning Engineer job description
    with open(SAMPLE_JOBS_FILE, "r") as f:
        jobs = json.load(f)
    ml_job = jobs["Senior Machine Learning Engineer"]["description"]

    # Gather all 7 synthetic demo files
    resume_files = sorted(list(SAMPLE_RESUMES_DIR.glob("candidate_*.pdf")))
    assert len(resume_files) >= 7

    # Run PDF extractions
    extractions = [PDFExtractor.extract_from_path(p) for p in resume_files]

    # Validate that edge-case files have appropriate statuses
    status_by_filename = {e.filename: e.status for e in extractions}
    assert status_by_filename["candidate_05_scanned_image_sample.pdf"] == ExtractionStatus.SCANNED_IMAGE
    assert status_by_filename["candidate_06_empty_sample.pdf"] == ExtractionStatus.EMPTY_FILE
    assert status_by_filename["candidate_07_corrupted_sample.pdf"] == ExtractionStatus.CORRUPTED_OR_INVALID

    # Run screening
    matcher = ResumeMatcher()
    results = matcher.screen_candidates(ml_job, extractions)

    assert len(results) == len(resume_files)

    # 1. Candidate 01 (Senior ML) should be the #1 ranked candidate
    assert results[0].filename == "candidate_01_aisha_sharma_senior_ml.pdf"
    assert results[0].rank == 1
    assert results[0].overall_score >= 50.0
    # Candidate 1 should have substantially higher score than Candidate 2
    assert results[0].overall_score > results[1].overall_score * 2
    assert "Machine Learning" in results[0].matched_skills
    assert "PyTorch" in results[0].matched_skills

    # 2. Check that unusable files are placed at bottom with score 0
    unusable_results = [r for r in results if not r.extraction.is_usable]
    assert len(unusable_results) == 3
    for r in unusable_results:
        assert r.overall_score == 0.0
        assert r.rank >= 5
