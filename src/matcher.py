"""
TalentLens AI — Resume Matching Engine
Calculates explainable matching scores combining TF-IDF cosine similarity,
direct skill coverage, and domain breadth bonuses with candidate ranking.
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.config import (
    DEFAULT_WEIGHT_TFIDF,
    DEFAULT_WEIGHT_SKILLS,
    DEFAULT_WEIGHT_BREADTH
)
from src.data_models import (
    ExtractionResult,
    CandidateResult,
    ScoringBreakdown
)
from src.skills_extractor import SkillsExtractor


class ResumeMatcher:
    """Computes TF-IDF vector representations, cosine similarity, and explainable scores."""

    def __init__(
        self,
        weight_tfidf: float = DEFAULT_WEIGHT_TFIDF,
        weight_skills: float = DEFAULT_WEIGHT_SKILLS,
        weight_breadth: float = DEFAULT_WEIGHT_BREADTH,
        skills_extractor: Optional[SkillsExtractor] = None
    ):
        self.weight_tfidf = weight_tfidf
        self.weight_skills = weight_skills
        self.weight_breadth = weight_breadth
        self.skills_extractor = skills_extractor or SkillsExtractor()

    def update_weights(self, weight_tfidf: float, weight_skills: float, weight_breadth: float) -> None:
        """Dynamically updates scoring weights ensuring they are non-negative."""
        self.weight_tfidf = max(0.0, weight_tfidf)
        self.weight_skills = max(0.0, weight_skills)
        self.weight_breadth = max(0.0, weight_breadth)

    def compute_tfidf_similarity(
        self,
        job_description: str,
        resumes_text: List[str]
    ) -> Tuple[np.ndarray, TfidfVectorizer, Any]:
        """
        Fits TfidfVectorizer over job description and resume corpus.
        Returns cosine similarity vector between JD and each resume.
        """
        corpus = [job_description] + resumes_text
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000,
            sublinear_tf=True
        )
        
        tfidf_matrix = vectorizer.fit_transform(corpus)
        jd_vector = tfidf_matrix[0:1]
        resume_vectors = tfidf_matrix[1:]
        
        similarities = cosine_similarity(jd_vector, resume_vectors)[0]
        return similarities, vectorizer, tfidf_matrix

    def get_top_overlapping_terms(
        self,
        vectorizer: TfidfVectorizer,
        jd_tfidf_vector: Any,
        resume_tfidf_vector: Any,
        top_n: int = 8
    ) -> List[Dict[str, Any]]:
        """
        Calculates the top terms contributing to TF-IDF cosine similarity
        by computing element-wise dot product of the two vectors.
        """
        feature_names = vectorizer.get_feature_names_out()
        jd_dense = jd_tfidf_vector.toarray().flatten()
        res_dense = resume_tfidf_vector.toarray().flatten()
        
        # Contribution is product of normalized TF-IDF weights
        contributions = jd_dense * res_dense
        top_indices = np.argsort(contributions)[::-1]
        
        results = []
        for idx in top_indices:
            score = float(contributions[idx])
            if score <= 0.0:
                break
            results.append({
                "term": feature_names[idx],
                "contribution": round(score, 4),
                "jd_weight": round(float(jd_dense[idx]), 4),
                "resume_weight": round(float(res_dense[idx]), 4)
            })
            if len(results) >= top_n:
                break
                
        return results

    def score_candidate(
        self,
        tfidf_similarity: float,
        skill_comparison: Dict[str, Any]
    ) -> ScoringBreakdown:
        """
        Calculates the explainable matching score (0 to 100) and formula breakdown.
        """
        # TF-IDF similarity is [0.0, 1.0], scale to [0, 100]
        tfidf_score = round(float(np.clip(tfidf_similarity * 100.0, 0.0, 100.0)), 1)
        
        # Skill match score: percentage of JD skills satisfied by candidate
        jd_skills_count = skill_comparison.get("jd_skills_count", 0)
        matched_count = skill_comparison.get("matched_count", 0)
        
        if jd_skills_count > 0:
            skill_match_score = round((matched_count / jd_skills_count) * 100.0, 1)
        else:
            # If JD explicitly specified 0 taxonomy skills, align with TF-IDF score
            skill_match_score = tfidf_score

        # Breadth bonus: up to 10 points for complementary domain skills
        additional_count = skill_comparison.get("additional_count", 0)
        breadth_bonus = round(float(min(10.0, additional_count * 1.5)), 1)

        # Weighted calculation
        tfidf_pts = tfidf_score * self.weight_tfidf
        skill_pts = skill_match_score * self.weight_skills
        breadth_pts = breadth_bonus * self.weight_breadth
        
        total_unnormalized = tfidf_pts + skill_pts + breadth_pts
        total_score = round(float(np.clip(total_unnormalized, 0.0, 100.0)), 1)

        formula = (
            f"({tfidf_score:.1f} × {self.weight_tfidf:.2f}) + "
            f"({skill_match_score:.1f} × {self.weight_skills:.2f}) + "
            f"({breadth_bonus:.1f} × {self.weight_breadth:.2f}) = "
            f"{total_score:.1f} / 100"
        )

        return ScoringBreakdown(
            overall_score=total_score,
            tfidf_score=tfidf_score,
            skill_match_score=skill_match_score,
            breadth_bonus=breadth_bonus,
            weight_tfidf=self.weight_tfidf,
            weight_skills=self.weight_skills,
            weight_breadth=self.weight_breadth,
            tfidf_points=round(tfidf_pts, 2),
            skill_points=round(skill_pts, 2),
            breadth_points=round(breadth_pts, 2),
            formula_explanation=formula
        )

    def screen_candidates(
        self,
        job_description: str,
        extractions: List[ExtractionResult]
    ) -> List[CandidateResult]:
        """
        Screens a batch of extracted resumes against a job description.
        Computes TF-IDF similarity, extracts skills, calculates explainable scores,
        and ranks candidates from top to bottom.
        """
        if not extractions:
            return []

        usable_extractions = [e for e in extractions if e.is_usable]
        unusable_extractions = [e for e in extractions if not e.is_usable]

        candidate_results = []

        if usable_extractions:
            if job_description.strip():
                usable_texts = [e.clean_text for e in usable_extractions]
                similarities, vectorizer, tfidf_matrix = self.compute_tfidf_similarity(
                    job_description, usable_texts
                )
                jd_vector = tfidf_matrix[0:1]

                for idx, ext in enumerate(usable_extractions):
                    sim = similarities[idx]
                    skill_comp = self.skills_extractor.compare_skills(job_description, ext.clean_text)
                    score_breakdown = self.score_candidate(sim, skill_comp)
                    
                    # Compute top contributing TF-IDF terms
                    resume_vector = tfidf_matrix[idx + 1: idx + 2]
                    top_terms = self.get_top_overlapping_terms(vectorizer, jd_vector, resume_vector)

                    candidate_results.append(CandidateResult(
                        rank=0,  # Assigned after sorting
                        filename=ext.filename,
                        overall_score=score_breakdown.overall_score,
                        score_breakdown=score_breakdown,
                        extraction=ext,
                        matched_skills=skill_comp["matched_skills"],
                        missing_skills=skill_comp["missing_skills"],
                        additional_skills=skill_comp["additional_skills"],
                        top_overlapping_terms=top_terms
                    ))
            else:
                for ext in usable_extractions:
                    empty_breakdown = ScoringBreakdown(
                        overall_score=0.0,
                        tfidf_score=0.0,
                        skill_match_score=0.0,
                        breadth_bonus=0.0,
                        weight_tfidf=self.weight_tfidf,
                        weight_skills=self.weight_skills,
                        weight_breadth=self.weight_breadth,
                        tfidf_points=0.0,
                        skill_points=0.0,
                        breadth_points=0.0,
                        formula_explanation="Cannot score: Job description is empty"
                    )
                    candidate_results.append(CandidateResult(
                        rank=0,
                        filename=ext.filename,
                        overall_score=0.0,
                        score_breakdown=empty_breakdown,
                        extraction=ext,
                        matched_skills=[],
                        missing_skills=[],
                        additional_skills=[],
                        top_overlapping_terms=[]
                    ))

        # Sort usable candidates by overall score descending
        candidate_results.sort(key=lambda c: c.overall_score, reverse=True)

        # Assign ranks
        for rank_idx, candidate in enumerate(candidate_results, start=1):
            candidate.rank = rank_idx

        # Append unusable documents with clear error status and score 0.0
        for ext in unusable_extractions:
            dummy_breakdown = ScoringBreakdown(
                overall_score=0.0,
                tfidf_score=0.0,
                skill_match_score=0.0,
                breadth_bonus=0.0,
                weight_tfidf=self.weight_tfidf,
                weight_skills=self.weight_skills,
                weight_breadth=self.weight_breadth,
                tfidf_points=0.0,
                skill_points=0.0,
                breadth_points=0.0,
                formula_explanation=f"Cannot score: {ext.status.value}"
            )
            candidate_results.append(CandidateResult(
                rank=len(candidate_results) + 1,
                filename=ext.filename,
                overall_score=0.0,
                score_breakdown=dummy_breakdown,
                extraction=ext,
                matched_skills=[],
                missing_skills=[],
                additional_skills=[],
                top_overlapping_terms=[]
            ))

        return candidate_results
