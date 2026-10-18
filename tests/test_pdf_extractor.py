"""
Unit tests for PDFExtractor.
Verifies digital text extraction, error handling for corrupt files,
empty file detection, and scanned image detection.
"""

import pytest
from pathlib import Path
from src.pdf_extractor import PDFExtractor
from src.data_models import ExtractionStatus
from src.config import SAMPLE_RESUMES_DIR


def test_clean_text_normalizes_whitespace():
    raw = "Senior   Python\t\tDeveloper\r\n\r\n\n\nMachine   Learning \xa0 Specialist"
    cleaned = PDFExtractor.clean_text(raw)
    assert "Senior Python Developer" in cleaned
    assert "Machine Learning Specialist" in cleaned
    assert "\r" not in cleaned
    assert "\xa0" not in cleaned


def test_clean_text_handles_control_chars():
    raw = "Valid Text \x00\x05\x1f With Hidden Control Chars"
    cleaned = PDFExtractor.clean_text(raw)
    assert cleaned == "Valid Text With Hidden Control Chars"


def test_extract_valid_pdf():
    valid_pdf = SAMPLE_RESUMES_DIR / "candidate_01_aisha_sharma_senior_ml.pdf"
    assert valid_pdf.exists()
    
    result = PDFExtractor.extract_from_path(valid_pdf)
    assert result.status == ExtractionStatus.SUCCESS
    assert result.is_usable is True
    assert result.page_count >= 1
    assert "Aisha Sharma" in result.clean_text
    assert "Machine Learning" in result.clean_text
    assert result.char_count > 100


def test_extract_scanned_image_pdf():
    scanned_pdf = SAMPLE_RESUMES_DIR / "candidate_05_scanned_image_sample.pdf"
    assert scanned_pdf.exists()

    result = PDFExtractor.extract_from_path(scanned_pdf)
    assert result.status == ExtractionStatus.SCANNED_IMAGE
    assert result.is_usable is False
    assert result.image_count >= 1
    assert "Scanned image PDF detected" in result.error_message


def test_extract_empty_pdf():
    empty_pdf = SAMPLE_RESUMES_DIR / "candidate_06_empty_sample.pdf"
    assert empty_pdf.exists()

    result = PDFExtractor.extract_from_path(empty_pdf)
    assert result.status == ExtractionStatus.EMPTY_FILE
    assert result.is_usable is False
    assert result.char_count < 10


def test_extract_corrupted_pdf():
    corrupt_pdf = SAMPLE_RESUMES_DIR / "candidate_07_corrupted_sample.pdf"
    assert corrupt_pdf.exists()

    result = PDFExtractor.extract_from_path(corrupt_pdf)
    assert result.status == ExtractionStatus.CORRUPTED_OR_INVALID
    assert result.is_usable is False
    assert result.error_message is not None


def test_extract_from_empty_bytes():
    result = PDFExtractor.extract_from_bytes(b"", filename="zero_byte.pdf")
    assert result.status == ExtractionStatus.EMPTY_FILE
    assert result.is_usable is False
    assert "empty" in result.error_message.lower()


def test_extract_from_invalid_bytes():
    result = PDFExtractor.extract_from_bytes(b"NOT A REAL PDF CONTENT RANDOM BYTES", filename="garbage.pdf")
    assert result.status == ExtractionStatus.CORRUPTED_OR_INVALID
    assert result.is_usable is False
