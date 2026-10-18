"""
TalentLens AI — Data Models
Strongly-typed dataclasses and enums representing extraction states,
skill matches, and explainable scoring breakdowns.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional


class ExtractionStatus(str, Enum):
    """Lifecycle status of PDF text extraction."""
    SUCCESS = "Success"
    SCANNED_IMAGE = "Scanned / Image-Only PDF"
    EMPTY_FILE = "Empty / Blank PDF"
    CORRUPTED_OR_INVALID = "Corrupted or Invalid PDF"
    UNREADABLE = "Unreadable PDF"


@dataclass
class ExtractionResult:
    """Result of extracting text from a candidate PDF resume."""
    filename: str
    status: ExtractionStatus
    raw_text: str = ""
    clean_text: str = ""
    page_count: int = 0
    image_count: int = 0
    char_count: int = 0
    error_message: Optional[str] = None

    @property
    def is_usable(self) -> bool:
        """True if sufficient readable text was extracted for screening."""
        return self.status == ExtractionStatus.SUCCESS and len(self.clean_text.strip()) > 0


@dataclass
class ScoringBreakdown:
    """Detailed explainable breakdown of the candidate's matching score."""
    overall_score: float                # 0 - 100
    tfidf_score: float                  # 0 - 100
    skill_match_score: float            # 0 - 100
    breadth_bonus: float                # 0 - 10
    
    # Active weights applied
    weight_tfidf: float
    weight_skills: float
    weight_breadth: float
    
    # Contribution points
    tfidf_points: float                 # tfidf_score * weight_tfidf
    skill_points: float                 # skill_match_score * weight_skills
    breadth_points: float               # breadth_bonus * weight_breadth

    # Explanation formula string
    formula_explanation: str = ""


@dataclass
class CandidateResult:
    """Complete screening result for an individual candidate."""
    rank: int
    filename: str
    overall_score: float
    score_breakdown: ScoringBreakdown
    extraction: ExtractionResult
    
    # Skills analysis
    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    additional_skills: List[str] = field(default_factory=list)
    
    # Top keywords / TF-IDF terms overlapping with JD
    top_overlapping_terms: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def tier(self) -> str:
        """Categorize into an explainable descriptive tier."""
        if self.overall_score >= 75.0:
            return "Strong Match"
        elif self.overall_score >= 50.0:
            return "Moderate Match"
        elif self.overall_score >= 30.0:
            return "Partial Match"
        else:
            return "Low Alignment"
