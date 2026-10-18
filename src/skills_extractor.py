"""
TalentLens AI — Skills Extractor
Extracts technical and professional skills using a configurable taxonomy
with robust multi-word phrase matching and symbol-aware regex patterns.
"""

import re
from typing import Dict, List, Set, Any, Optional

from src.config import DEFAULT_SKILLS_TAXONOMY


class SkillsExtractor:
    """Configurable skill extraction engine based on curated skill taxonomies and regex."""

    def __init__(self, taxonomy: Optional[Dict[str, Dict[str, List[str]]]] = None):
        """
        Initializes extractor with a taxonomy:
        {
            "Category Name": {
                "Canonical Skill": ["alias1", "alias2", ...]
            }
        }
        """
        self.taxonomy = taxonomy or DEFAULT_SKILLS_TAXONOMY
        self._compiled_patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        Compiles optimized regex patterns for each canonical skill and alias.
        Carefully handles symbols like C++, C#, .NET, CI/CD, and single-letter languages.
        """
        patterns = {}
        for category, skills in self.taxonomy.items():
            for canonical_name, aliases in skills.items():
                alias_patterns = []
                for alias in aliases:
                    alias_clean = alias.strip().lower()
                    # Custom boundaries for symbols (+, #, ., /)
                    escaped = re.escape(alias_clean)
                    
                    # If alias ends/starts with non-word character (like C++, C#, .NET, CI/CD)
                    prefix = r'(?<![a-zA-Z0-9])'
                    suffix = r'(?![a-zA-Z0-9])'
                    
                    # Multi-space normalization
                    escaped = re.sub(r'\\ ', r'\\s+', escaped)
                    pattern_str = f"{prefix}{escaped}{suffix}"
                    alias_patterns.append(re.compile(pattern_str, re.IGNORECASE))
                
                patterns[canonical_name] = {
                    "category": category,
                    "compiled": alias_patterns,
                    "canonical_name": canonical_name
                }
        return patterns

    def add_custom_skill(self, category: str, canonical_name: str, aliases: List[str]) -> None:
        """Dynamically adds a user-defined skill to the active taxonomy."""
        if category not in self.taxonomy:
            self.taxonomy[category] = {}
        all_aliases = list(set([canonical_name.lower()] + [a.lower().strip() for a in aliases if a.strip()]))
        self.taxonomy[category][canonical_name] = all_aliases
        self._compiled_patterns = self._compile_patterns()

    def extract_skills(self, text: str) -> Dict[str, Dict[str, Any]]:
        """
        Extracts skills from text and returns dictionary:
        {
            "Python": {"category": "Programming Languages", "matched_aliases": ["python", "py"]}
        }
        """
        if not text or not text.strip():
            return {}

        results = {}
        # Pre-normalize whitespace in target text
        normalized_text = " " + re.sub(r'\s+', ' ', text.lower()) + " "

        for canonical_name, meta in self._compiled_patterns.items():
            matched_aliases = []
            for pattern in meta["compiled"]:
                matches = pattern.findall(normalized_text)
                if matches:
                    matched_aliases.extend(matches)
            
            if matched_aliases:
                results[canonical_name] = {
                    "category": meta["category"],
                    "matched_aliases": sorted(list(set(matched_aliases)))
                }

        return results

    def extract_skills_set(self, text: str) -> Set[str]:
        """Returns a set of canonical skill names found in the text."""
        return set(self.extract_skills(text).keys())

    def compare_skills(self, job_description_text: str, resume_text: str) -> Dict[str, Any]:
        """
        Compares skills present in the Job Description against the Resume.
        Returns:
            - jd_skills: list of skills extracted from JD
            - resume_skills: list of skills extracted from Resume
            - matched_skills: intersection of JD and Resume skills
            - missing_skills: skills present in JD but absent from Resume
            - additional_skills: skills present in Resume not in JD
            - match_ratio: float (0.0 to 1.0)
        """
        jd_skills_dict = self.extract_skills(job_description_text)
        resume_skills_dict = self.extract_skills(resume_text)

        jd_set = set(jd_skills_dict.keys())
        resume_set = set(resume_skills_dict.keys())

        matched = sorted(list(jd_set.intersection(resume_set)))
        missing = sorted(list(jd_set - resume_set))
        additional = sorted(list(resume_set - jd_set))

        match_ratio = len(matched) / len(jd_set) if len(jd_set) > 0 else 0.0

        return {
            "jd_skills": sorted(list(jd_set)),
            "resume_skills": sorted(list(resume_set)),
            "matched_skills": matched,
            "missing_skills": missing,
            "additional_skills": additional,
            "match_ratio": match_ratio,
            "jd_skills_count": len(jd_set),
            "matched_count": len(matched),
            "missing_count": len(missing),
            "additional_count": len(additional)
        }
