"""
TalentLens AI — Synthetic Demo Resume Generator
Uses PyMuPDF to generate realistic candidate PDF resumes with varied skill sets,
as well as synthetic edge-case documents (scanned image, empty, and corrupted).
All data is 100% synthetic and created for educational/demonstration purposes.
"""

from pathlib import Path
import pymupdf

OUTPUT_DIR = Path(__file__).resolve().parent / "resumes"


def create_text_pdf(filepath: Path, title: str, sections: list) -> None:
    """Creates a clean, formatted digital PDF resume using PyMuPDF."""
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)  # Standard Letter size

    # Header styling
    page.insert_text(pymupdf.Point(50, 50), title, fontsize=18, fontname="helv", color=(0.1, 0.2, 0.4))
    page.draw_line(pymupdf.Point(50, 60), pymupdf.Point(562, 60), color=(0.7, 0.7, 0.7), width=1)

    y = 80
    for section_title, content in sections:
        # Section header
        page.insert_text(pymupdf.Point(50, y), section_title.upper(), fontsize=11, fontname="helv", color=(0.2, 0.4, 0.7))
        y += 16
        
        # Section content lines
        for line in content:
            # Word wrapping simple simulation
            page.insert_text(pymupdf.Point(55, y), line, fontsize=9.5, fontname="helv", color=(0.15, 0.15, 0.15))
            y += 13
        y += 12

    doc.save(str(filepath))
    doc.close()
    print(f"Generated text resume: {filepath.name}")


def create_scanned_pdf(filepath: Path) -> None:
    """
    Creates a simulated scanned PDF where text is rendered into a bitmap image
    and inserted onto the page with NO selectable digital text layer.
    """
    # First create temporary page with text
    temp_doc = pymupdf.open()
    page = temp_doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(50, 70), "SCANNED CANDIDATE RESUME — OCR REQUIRED", fontsize=14, fontname="helv")
    page.insert_text(pymupdf.Point(50, 100), "Candidate Name: Alex Mercer (Photocopied Resume)", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(50, 120), "Skills: Java, C++, SQL, Machine Learning", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(50, 140), "Experience: 5 years software engineer at Tech Corp.", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(50, 160), "Notice: This document was scanned and has no digital font layer.", fontsize=10, fontname="helv")

    # Render page to raster pixmap image
    pix = page.get_pixmap(dpi=150)
    image_bytes = pix.tobytes("png")
    temp_doc.close()

    # Now create the final target PDF and insert ONLY the image
    scanned_doc = pymupdf.open()
    scanned_page = scanned_doc.new_page(width=612, height=792)
    scanned_page.insert_image(pymupdf.Rect(50, 50, 562, 742), stream=image_bytes)
    scanned_doc.save(str(filepath))
    scanned_doc.close()
    print(f"Generated simulated scanned PDF: {filepath.name}")


def create_empty_pdf(filepath: Path) -> None:
    """Creates a blank 1-page PDF document containing zero text and zero images."""
    doc = pymupdf.open()
    doc.new_page(width=612, height=792)
    doc.save(str(filepath))
    doc.close()
    print(f"Generated empty/blank PDF: {filepath.name}")


def create_corrupt_pdf(filepath: Path) -> None:
    """Creates an intentionally corrupted binary file with invalid PDF headers/structure."""
    with open(filepath, "wb") as f:
        f.write(b"%PDF-1.4 [MALFORMED STREAM DATA \x00\xff\xee\xdd NOT A VALID TRAILER EOF")
    print(f"Generated corrupted/invalid PDF: {filepath.name}")


def generate_all_samples():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Candidate 01: Senior ML Engineer (High Match for ML role)
    create_text_pdf(
        OUTPUT_DIR / "candidate_01_aisha_sharma_senior_ml.pdf",
        "Aisha Sharma — Senior Machine Learning Engineer",
        [
            ("Professional Summary", [
                "Senior Machine Learning Engineer with 6+ years of experience in architecting NLP models,",
                "productionizing Deep Learning systems, and implementing Retrieval-Augmented Generation (RAG).",
                "Proven track record scaling PyTorch and Scikit-Learn pipelines to millions of daily inference calls."
            ]),
            ("Core Technical Skills", [
                "Languages & Frameworks: Python, PyTorch, Scikit-Learn, TensorFlow, Pandas, NumPy, Keras",
                "AI / ML Specializations: Machine Learning, Deep Learning, Natural Language Processing (NLP),",
                "Transformers, Large Language Models (LLMs), RAG, Prompt Engineering, Model Evaluation",
                "Engineering & Cloud: Docker, Kubernetes, REST API, Git, GitHub Actions, Linux, AWS (S3, EC2, Lambda)",
                "Methodologies: Agile, Scrum, Unit Testing with Pytest, Microservices Architecture"
            ]),
            ("Professional Experience", [
                "Lead AI Engineer | Synapse Analytics (2021 - Present)",
                "- Designed enterprise RAG question-answering system using Hugging Face Transformers and PyTorch.",
                "- Reduced model latency by 45% containerizing inference services using Docker and FastAPI REST APIs.",
                "- Mentored team of 5 data scientists and implemented automated CI/CD unit testing with Pytest.",
                "",
                "Machine Learning Scientist | DataFlow Labs (2018 - 2021)",
                "- Built tabular predictive pipelines using Scikit-Learn, XGBoost, Pandas, and NumPy.",
                "- Engineered end-to-end NLP text classification workflows processing 500k+ documents monthly."
            ]),
            ("Education & Certifications", [
                "M.S. in Computer Science (Artificial Intelligence) — Stanford University",
                "AWS Certified Machine Learning Specialist"
            ])
        ]
    )

    # 2. Candidate 02: Data Analyst / Data Scientist (Moderate Match for ML role, High for BI)
    create_text_pdf(
        OUTPUT_DIR / "candidate_02_david_chen_data_analyst.pdf",
        "David Chen — Data Analyst & Quantitative Specialist",
        [
            ("Professional Summary", [
                "Analytical problem solver with 4 years of experience extracting business value from raw data.",
                "Expertise in SQL query optimization, exploratory data analysis using Python and Pandas, and building",
                "executive dashboards in Power BI and Tableau. Applied foundational Scikit-Learn algorithms for customer churn."
            ]),
            ("Technical Skills", [
                "Analytics & Querying: SQL, PostgreSQL, MySQL, Data Analysis, Exploratory Data Analysis, Excel",
                "Scripting & Tools: Python, Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn, Git",
                "Business Intelligence: Power BI, Tableau, Data Visualization, Statistical Analysis, Hypothesis Testing",
                "Practices: Agile, Jira, Business Intelligence reporting, A/B Testing"
            ]),
            ("Experience", [
                "Senior Data Analyst | MetricPulse Analytics (2021 - Present)",
                "- Designed 15+ automated interactive dashboards in Power BI and Tableau for C-suite stakeholders.",
                "- Wrote complex SQL procedures and Python ETL pipelines with Pandas to aggregate financial metrics.",
                "- Built baseline customer churn classification models using Scikit-Learn logistic regression.",
                "",
                "Data Analytics Associate | RetailInsight Inc. (2019 - 2021)",
                "- Conducted statistical hypothesis tests and exploratory analysis on large consumer transaction sets.",
                "- Automated weekly executive summary reports using Excel VBA and Python scripts."
            ]),
            ("Education", [
                "B.S. in Statistics and Applied Mathematics — University of Washington"
            ])
        ]
    )

    # 3. Candidate 03: Full Stack Web Developer (Low Match for ML role, High for Web role)
    create_text_pdf(
        OUTPUT_DIR / "candidate_03_elena_rodriguez_fullstack_dev.pdf",
        "Elena Rodriguez — Full Stack Web Developer",
        [
            ("Professional Summary", [
                "Full Stack Web Developer with 5 years building scalable web applications and responsive user interfaces.",
                "Specialized in React, TypeScript, Node.js, and Express with PostgreSQL backends. Strong focus on clean code,",
                "REST API architecture, Docker containerization, and modern frontend styling."
            ]),
            ("Technical Competencies", [
                "Frontend: JavaScript, TypeScript, React, HTML/CSS, Tailwind CSS, Bootstrap, Redux",
                "Backend & APIs: Node.js, Express, REST API, GraphQL, Microservices",
                "Databases: PostgreSQL, MySQL, MongoDB, Redis",
                "DevOps & Tools: Docker, Git, GitHub Actions, Linux, CI/CD, Jest, Agile / Scrum"
            ]),
            ("Work Experience", [
                "Senior Frontend & Full Stack Developer | AppVenture Studio (2021 - Present)",
                "- Built responsive enterprise web application from scratch using React, TypeScript, and Tailwind CSS.",
                "- Architected Node.js and Express microservice backends connected to PostgreSQL and Redis caches.",
                "- Configured Docker development containers and automated deployment pipelines using GitHub Actions.",
                "",
                "Web Developer | Nexus Interactive (2019 - 2021)",
                "- Developed client-facing portals using modern JavaScript, HTML5, CSS3, and RESTful APIs.",
                "- Maintained high test coverage with Jest unit testing and participated in 2-week Agile sprints."
            ]),
            ("Education", [
                "B.S. in Computer Science — University of Texas at Austin"
            ])
        ]
    )

    # 4. Candidate 04: Cloud & DevOps Engineer
    create_text_pdf(
        OUTPUT_DIR / "candidate_04_marcus_vance_cloud_devops.pdf",
        "Marcus Vance — Cloud & DevOps Infrastructure Engineer",
        [
            ("Professional Summary", [
                "Infrastructure and DevOps Engineer with 6 years experience automating cloud platforms on AWS.",
                "Specialist in Infrastructure as Code (Terraform), Kubernetes cluster orchestration, Docker containerization,",
                "and robust CI/CD pipeline automation with Git and Linux Shell scripting."
            ]),
            ("Technical Skills", [
                "Cloud Providers: AWS (EC2, S3, EKS, Lambda, IAM), Google Cloud Platform (GCP)",
                "Containers & Orchestration: Docker, Kubernetes, Helm",
                "Automation & CI/CD: Terraform, Ansible, CI/CD, GitHub Actions, Jenkins, Git",
                "OS & Scripting: Linux (Ubuntu, RHEL), Shell / Bash, Python, PowerShell",
                "Monitoring & Practices: Prometheus, Grafana, Microservices, Agile"
            ]),
            ("Experience", [
                "Lead DevOps Engineer | CloudScale Networks (2020 - Present)",
                "- Provisioned multi-region AWS cloud infrastructure using modular Terraform scripts.",
                "- Migrated monolithic workloads to Kubernetes (EKS) and Docker, cutting compute costs by 35%.",
                "- Engineered end-to-end CI/CD pipelines deploying microservices across testing and production environments.",
                "",
                "Systems & Cloud Administrator | Horizon Telecom (2018 - 2020)",
                "- Administered 200+ Linux enterprise servers and automated routine health checks with Python and Bash.",
                "- Managed Git repository branching strategies and assisted developers with container troubleshooting."
            ]),
            ("Education & Certifications", [
                "B.S. in Information Systems — Purdue University",
                "AWS Certified Solutions Architect — Professional",
                "Certified Kubernetes Administrator (CKA)"
            ])
        ]
    )

    # 5. Candidate 05: Scanned Image PDF (simulates photocopied resume without text layer)
    create_scanned_pdf(OUTPUT_DIR / "candidate_05_scanned_image_sample.pdf")

    # 6. Candidate 06: Blank / Empty PDF
    create_empty_pdf(OUTPUT_DIR / "candidate_06_empty_sample.pdf")

    # 7. Candidate 07: Corrupted / Invalid Binary PDF
    create_corrupt_pdf(OUTPUT_DIR / "candidate_07_corrupted_sample.pdf")

    print("\nAll synthetic demo test files generated successfully in sample_data/resumes/")


if __name__ == "__main__":
    generate_all_samples()
