"""
Unit tests for SkillsExtractor.
Verifies canonical skill detection, multi-word matching, symbol handling (C++, C#, .NET),
dynamic custom skills, and JD comparison logic.
"""

import pytest
from src.skills_extractor import SkillsExtractor


@pytest.fixture
def extractor():
    return SkillsExtractor()


def test_extract_basic_skills(extractor):
    text = "Candidate has strong experience with Python, Pandas, and NumPy."
    skills = extractor.extract_skills_set(text)
    assert "Python" in skills
    assert "Pandas" in skills
    assert "NumPy" in skills
    assert "Java" not in skills


def test_extract_tricky_symbols(extractor):
    text = "Developing high-performance microservices in C++ and C# with .NET backends."
    skills = extractor.extract_skills_set(text)
    assert "C++" in skills
    assert "C#" in skills


def test_extract_multi_word_phrases(extractor):
    text = "Applied Natural Language Processing and Large Language Models for automated customer care."
    skills = extractor.extract_skills_set(text)
    assert "Natural Language Processing" in skills
    assert "Large Language Models" in skills


def test_extract_cloud_and_devops(extractor):
    text = "Managed Docker containers on Kubernetes with CI/CD automation via Git and Terraform on AWS."
    skills = extractor.extract_skills_set(text)
    assert "Docker" in skills
    assert "Kubernetes" in skills
    assert "CI/CD" in skills
    assert "AWS" in skills
    assert "Git" in skills
    assert "Terraform" in skills


def test_compare_skills(extractor):
    jd = "Required: Python, PyTorch, Docker, Kubernetes, SQL"
    resume = "I have hands-on experience in Python, PyTorch, SQL, and Pandas with Git."
    
    comp = extractor.compare_skills(jd, resume)
    
    # Matched: Python, PyTorch, SQL
    assert set(comp["matched_skills"]) == {"Python", "PyTorch", "SQL"}
    # Missing: Docker, Kubernetes
    assert set(comp["missing_skills"]) == {"Docker", "Kubernetes"}
    # Additional: Pandas, Git
    assert set(comp["additional_skills"]) == {"Pandas", "Git"}
    # Match ratio: 3 / 5 = 0.6
    assert pytest.approx(comp["match_ratio"], 0.01) == 0.6


def test_add_custom_skill(extractor):
    text = "Working extensively with Solidity smart contracts and Web3 protocols."
    
    # Before adding
    assert "Solidity" not in extractor.extract_skills_set(text)
    
    # Add custom skill
    extractor.add_custom_skill(
        category="Blockchain",
        canonical_name="Solidity",
        aliases=["solidity", "solidity smart contracts"]
    )
    
    # After adding
    skills = extractor.extract_skills_set(text)
    assert "Solidity" in skills


def test_contextual_pandas_and_numpy_aliases(extractor):
    # Contextual import / dataframe
    text_code = "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame(data)\narr = np.array([1, 2, 3])"
    skills = extractor.extract_skills_set(text_code)
    assert "Pandas" in skills
    assert "NumPy" in skills

    # Parenthetical alias
    text_paren = "Experienced with Python (pandas/pd) and numpy (np) libraries."
    skills_paren = extractor.extract_skills_set(text_paren)
    assert "Pandas" in skills_paren
    assert "NumPy" in skills_paren

    # Unrelated 'pd' should NOT match Pandas
    unrelated_text = "PS ID: 26003 PD score: 40 paid in full"
    skills_unrelated = extractor.extract_skills_set(unrelated_text)
    assert "Pandas" not in skills_unrelated


def test_power_bi_and_data_visualization_aliases(extractor):
    # Power BI variations
    text_bi = "Built executive dashboards using Microsoft Power BI Desktop and PowerBI Service."
    skills_bi = extractor.extract_skills_set(text_bi)
    assert "Power BI" in skills_bi

    # British spelling and dataviz variations
    text_viz = "Specialized in data visualisation, dataviz, and interactive charts with Plotly and Seaborn."
    skills_viz = extractor.extract_skills_set(text_viz)
    assert "Data Visualization" in skills_viz

    # Data Analysis and analytics
    text_ana = "Performed exploratory data analysis (EDA) and data analytics on financial datasets."
    skills_ana = extractor.extract_skills_set(text_ana)
    assert "Data Analysis" in skills_ana

