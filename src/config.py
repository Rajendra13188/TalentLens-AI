"""
TalentLens AI — Configuration and Constants
Defines default weights, skill taxonomy, ethical disclaimers, and threshold parameters.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
SAMPLE_RESUMES_DIR = SAMPLE_DATA_DIR / "resumes"
SAMPLE_JOBS_FILE = SAMPLE_DATA_DIR / "sample_jobs.json"

# PDF Extraction Thresholds
SCANNED_PDF_CHAR_THRESHOLD = 40  # Minimum characters extracted before flagging as scanned/image
EMPTY_PDF_CHAR_THRESHOLD = 10     # Threshold for empty/blank document

# Default Scoring Weights
DEFAULT_WEIGHT_TFIDF = 0.50       # 50% for TF-IDF contextual similarity
DEFAULT_WEIGHT_SKILLS = 0.40      # 40% for direct JD skill match
DEFAULT_WEIGHT_BREADTH = 0.10     # 10% for relevant skill breadth

# Mandatory Ethical & Educational Disclaimers
DISCLAIMER_TFIDF = (
    "TF-IDF cosine similarity measures text and vocabulary overlap between the resume "
    "and the job description. It is NOT a probability of candidate job success, competency, "
    "or future job performance."
)

DISCLAIMER_SKILL_ABSENCE = (
    "'Skill Not Detected' means the specified keyword or its known aliases were not found in the "
    "extracted digital text. It does NOT imply that the candidate definitely lacks that skill or "
    "cannot perform the required tasks."
)

DISCLAIMER_FAIRNESS = (
    "TalentLens AI ranks candidates purely on demonstrable technical skills and textual alignment "
    "with the job description. Protected personal characteristics (including gender, race, age, religion, "
    "and demographic attributes) are strictly excluded from ranking calculations."
)

DISCLAIMER_PRIVACY = (
    "All uploaded resume files are processed in-memory during the active browser session. "
    "Resumes are not permanently retained on disk or sent to any external server or API."
)

# Comprehensive Pre-configured Skills Taxonomy
DEFAULT_SKILLS_TAXONOMY = {
    "Programming Languages": {
        "Python": ["python", "py", "python3"],
        "JavaScript": ["javascript", "js", "ecmascript"],
        "TypeScript": ["typescript", "ts"],
        "Java": ["java", "core java", "j2ee"],
        "C++": ["c++", "cpp"],
        "C#": ["c#", "csharp", ".net"],
        "C": ["c programming", "c language"],
        "Go": ["golang", "go programming", "go lang"],
        "Rust": ["rust", "rustlang"],
        "Ruby": ["ruby", "ruby on rails", "rails"],
        "PHP": ["php", "laravel"],
        "SQL": ["sql", "tsql", "plsql", "structured query language"],
        "R": ["r programming", "r language", "r-project"],
        "Kotlin": ["kotlin"],
        "Swift": ["swift", "swiftui"],
        "MATLAB": ["matlab"],
        "Shell / Bash": ["bash", "shell scripting", "powershell", "zsh"],
        "HTML/CSS": ["html", "html5", "css", "css3"]
    },
    "Machine Learning & AI": {
        "Machine Learning": ["machine learning", "ml", "statistical learning"],
        "Deep Learning": ["deep learning", "neural networks", "dl"],
        "Natural Language Processing": ["nlp", "natural language processing", "text mining", "computational linguistics"],
        "Computer Vision": ["computer vision", "cv", "object detection", "image classification", "opencv"],
        "Scikit-Learn": ["scikit-learn", "sklearn"],
        "PyTorch": ["pytorch", "torch"],
        "TensorFlow": ["tensorflow", "tf"],
        "Keras": ["keras"],
        "Large Language Models": ["llm", "large language models", "prompt engineering", "genai", "generative ai"],
        "RAG": ["rag", "retrieval augmented generation", "vector search"],
        "Transformers": ["transformers", "hugging face", "bert", "gpt"],
        "Pandas": [
            "pandas", "pandas dataframe", "pandas library", "import pandas as pd",
            "pandas as pd", "pandas (pd)", "pandas/pd", "pd (pandas)",
            "pd.dataframe", "pd.series", "pd.read_csv", "pd.read_sql", "pd.concat", "pd.merge"
        ],
        "NumPy": [
            "numpy", "numpy array", "numpy library", "import numpy as np",
            "numpy as np", "numpy (np)", "numpy/np", "np (numpy)",
            "np.array", "np.ndarray", "np.zeros", "np.ones", "np.linspace"
        ],
        "XGBoost": ["xgboost", "lightgbm", "catboost"]
    },
    "Frameworks & Web Technologies": {
        "React": ["react", "react.js", "reactjs"],
        "Angular": ["angular", "angularjs"],
        "Vue.js": ["vue", "vue.js", "vuejs"],
        "Node.js": ["node", "node.js", "nodejs"],
        "Express": ["express", "express.js"],
        "Django": ["django"],
        "Flask": ["flask"],
        "FastAPI": ["fastapi"],
        "Spring Boot": ["spring boot", "spring framework", "spring"],
        "REST API": ["rest", "rest api", "restful api", "restful web services"],
        "GraphQL": ["graphql"],
        "Tailwind CSS": ["tailwind", "tailwind css", "tailwindcss"],
        "Bootstrap": ["bootstrap"]
    },
    "Cloud & DevOps": {
        "AWS": ["aws", "amazon web services", "ec2", "s3", "lambda"],
        "Azure": ["azure", "microsoft azure"],
        "Google Cloud Platform": ["gcp", "google cloud", "google cloud platform"],
        "Docker": ["docker", "containerization", "containers"],
        "Kubernetes": ["kubernetes", "k8s"],
        "CI/CD": ["ci/cd", "continuous integration", "continuous deployment", "jenkins", "github actions"],
        "Linux": ["linux", "ubuntu", "debian", "centos", "redhat"],
        "Terraform": ["terraform", "infrastructure as code", "iac"],
        "Git": ["git", "github", "gitlab", "version control"]
    },
    "Databases & Data Engineering": {
        "PostgreSQL": ["postgresql", "postgres"],
        "MySQL": ["mysql"],
        "MongoDB": ["mongodb", "mongo"],
        "Redis": ["redis"],
        "SQLite": ["sqlite"],
        "Elasticsearch": ["elasticsearch", "elastic search"],
        "Snowflake": ["snowflake"],
        "Apache Spark": ["spark", "pyspark", "apache spark"],
        "Kafka": ["kafka", "apache kafka"]
    },
    "Data Analysis & Visualization": {
        "Data Analysis": [
            "data analysis", "data analytics", "exploratory data analysis", "eda",
            "data analyst", "data analyze", "data analysing", "data analyzing"
        ],
        "Power BI": [
            "power bi", "powerbi", "power-bi", "microsoft power bi", "ms power bi",
            "power bi desktop", "power bi service", "power bi reports", "power bi dashboard"
        ],
        "Tableau": ["tableau", "tableau desktop", "tableau server"],
        "Excel": ["excel", "advanced excel", "microsoft excel", "ms excel", "spreadsheets"],
        "Data Visualization": [
            "data visualization", "data visualisation", "data viz", "dataviz",
            "data-visualization", "data-visualisation", "matplotlib", "seaborn",
            "plotly", "bokeh", "dashboarding", "visualizations", "visualisations"
        ],
        "Statistics": ["statistics", "statistical analysis", "hypothesis testing", "probability"]
    },
    "Software Engineering Practices": {
        "Agile / Scrum": ["agile", "scrum", "kanban", "sprint"],
        "Unit Testing": ["unit testing", "pytest", "test driven development", "tdd", "junit"],
        "Microservices": ["microservices", "microservice architecture"],
        "System Design": ["system design", "distributed systems", "software architecture"],
        "OOP": ["object-oriented programming", "oop", "object oriented design"]
    }
}
