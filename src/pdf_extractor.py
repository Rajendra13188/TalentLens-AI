"""
TalentLens AI — PDF Text Extractor
Uses PyMuPDF to extract text from PDF resumes while gracefully detecting
and handling corrupt files, empty documents, and scanned image PDFs.
"""

import io
import re
from pathlib import Path
from typing import Union, BinaryIO

import pymupdf

from src.config import SCANNED_PDF_CHAR_THRESHOLD, EMPTY_PDF_CHAR_THRESHOLD
from src.data_models import ExtractionResult, ExtractionStatus


class PDFExtractor:
    """Extracts text from PDF documents using PyMuPDF with comprehensive error handling."""

    @staticmethod
    def clean_text(raw_text: str) -> str:
        """
        Cleans extracted text by normalizing spaces, linebreaks,
        and non-printable characters.
        """
        if not raw_text:
            return ""
        
        # Replace non-breaking spaces and carriage returns
        text = raw_text.replace("\r\n", "\n").replace("\r", "\n").replace("\xa0", " ")
        
        # Remove null bytes and non-printable control characters (except newline, tab)
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
        
        # Collapse multiple horizontal whitespace characters
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Collapse excessive newlines (more than 2 consecutive newlines)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()

    @classmethod
    def extract_from_bytes(cls, file_bytes: bytes, filename: str = "uploaded_resume.pdf") -> ExtractionResult:
        """
        Extracts text from raw bytes in-memory without saving anything to disk.
        """
        if not file_bytes or len(file_bytes) == 0:
            return ExtractionResult(
                filename=filename,
                status=ExtractionStatus.EMPTY_FILE,
                error_message="The uploaded file is empty (0 bytes)."
            )

        doc = None
        try:
            # Open PDF in memory from byte stream
            doc = pymupdf.open(stream=file_bytes, filetype="pdf")
            return cls._process_document(doc, filename)

        except pymupdf.FileDataError as e:
            return ExtractionResult(
                filename=filename,
                status=ExtractionStatus.CORRUPTED_OR_INVALID,
                error_message=f"Invalid or corrupted PDF format: {str(e)}"
            )
        except Exception as e:
            return ExtractionResult(
                filename=filename,
                status=ExtractionStatus.CORRUPTED_OR_INVALID,
                error_message=f"Failed to read PDF document: {str(e)}"
            )
        finally:
            if doc is not None:
                doc.close()

    @classmethod
    def extract_from_path(cls, file_path: Union[str, Path]) -> ExtractionResult:
        """
        Extracts text from a local PDF file path.
        """
        path = Path(file_path)
        if not path.exists():
            return ExtractionResult(
                filename=path.name,
                status=ExtractionStatus.CORRUPTED_OR_INVALID,
                error_message=f"File not found on system: {path}"
            )
        
        if path.stat().st_size == 0:
            return ExtractionResult(
                filename=path.name,
                status=ExtractionStatus.EMPTY_FILE,
                error_message="File exists but is 0 bytes."
            )

        doc = None
        try:
            doc = pymupdf.open(str(path))
            return cls._process_document(doc, path.name)
        except pymupdf.FileDataError as e:
            return ExtractionResult(
                filename=path.name,
                status=ExtractionStatus.CORRUPTED_OR_INVALID,
                error_message=f"Invalid or corrupted PDF structure: {str(e)}"
            )
        except Exception as e:
            return ExtractionResult(
                filename=path.name,
                status=ExtractionStatus.CORRUPTED_OR_INVALID,
                error_message=f"Extraction failure: {str(e)}"
            )
        finally:
            if doc is not None:
                doc.close()

    @classmethod
    def _process_document(cls, doc: pymupdf.Document, filename: str) -> ExtractionResult:
        """
        Inspects pages, extracts text, counts images, and detects scanned/empty states.
        """
        page_count = doc.page_count
        if page_count == 0:
            return ExtractionResult(
                filename=filename,
                status=ExtractionStatus.EMPTY_FILE,
                page_count=0,
                error_message="PDF contains 0 pages."
            )

        raw_pages_text = []
        total_images = 0

        for page in doc:
            page_text = page.get_text()
            if page_text:
                raw_pages_text.append(page_text)
            
            # Count embedded images on this page
            images = page.get_images()
            total_images += len(images)

        full_raw_text = "\n".join(raw_pages_text)
        cleaned_text = cls.clean_text(full_raw_text)
        char_count = len(cleaned_text)

        # Detect Scanned / Image-Only PDF:
        # If very few characters extracted, but document contains images/drawings
        if char_count < SCANNED_PDF_CHAR_THRESHOLD and total_images > 0:
            return ExtractionResult(
                filename=filename,
                status=ExtractionStatus.SCANNED_IMAGE,
                raw_text=full_raw_text,
                clean_text=cleaned_text,
                page_count=page_count,
                image_count=total_images,
                char_count=char_count,
                error_message=(
                    f"Scanned image PDF detected ({total_images} image(s) found, only {char_count} "
                    f"text characters extracted). OCR is required to extract text from scanned images. "
                    f"Please provide a machine-readable digital PDF."
                )
            )

        # Detect completely empty or whitespace-only PDF
        if char_count < EMPTY_PDF_CHAR_THRESHOLD:
            return ExtractionResult(
                filename=filename,
                status=ExtractionStatus.EMPTY_FILE,
                raw_text=full_raw_text,
                clean_text=cleaned_text,
                page_count=page_count,
                image_count=total_images,
                char_count=char_count,
                error_message="The PDF contains no digital text characters or readable content."
            )

        # Successfully extracted digital text
        return ExtractionResult(
            filename=filename,
            status=ExtractionStatus.SUCCESS,
            raw_text=full_raw_text,
            clean_text=cleaned_text,
            page_count=page_count,
            image_count=total_images,
            char_count=char_count,
            error_message=None
        )
