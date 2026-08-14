# ============================================================
# ATS RESUME SCREENING SYSTEM
# CONFIGURATION
# ============================================================


# ============================================================
# 1. SKILL DATABASE
# ============================================================

SKILLS = [

    # Programming
    "Python",
    "Java",
    "C#",
    "C++",
    "SQL",
    "JavaScript",

    # .NET
    ".NET",
    ".NET Core",
    "ASP.NET",
    "ASP.NET Core",
    "Entity Framework",
    "Entity Framework Core",

    # Databases
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "SQL Server",
    "Oracle",

    # Backend
    "FastAPI",
    "Django",
    "Flask",
    "REST API",
    "GraphQL",

    # Cloud
    "AWS",
    "GCP",
    "Azure",
    "Azure Functions",
    "Azure API Management",
    "APIM",
    "Azure App Service",
    "Azure Storage",

    # AI
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Artificial Intelligence",
    "Generative AI",
    "LLM",
    "RAG",

    # Data
    "Pandas",
    "NumPy",
    "Scikit-Learn",
    "TensorFlow",
    "PyTorch",

    # Data Engineering
    "Spark",
    "PySpark",
    "ETL",
    "Data Engineering",
    "Data Analysis",
    "Data Science",

    # DevOps
    "Docker",
    "Kubernetes",
    "CI/CD",
    "Git",
    "GitHub",

    # Frontend
    "HTML",
    "CSS",
    "React",
    "Angular",

    # Visualization
    "Power BI",
    "Excel",
    "Tableau",

    # CS
    "OOP",
    "DSA",
    "Data Structures",
    "Algorithms",

    # Testing
    "Pytest",
    "Unit Testing",

    # API documentation
    "Swagger",
    "OpenAPI"
]


# ============================================================
# 2. EDUCATION KEYWORDS
# ============================================================

EDUCATION_KEYWORDS = [

    "b.tech",
    "btech",
    "b.e.",
    "be",
    "bachelor of technology",
    "bachelor's",
    "bachelor",

    "computer science",
    "data science",
    "information technology",
    "computer engineering",

    "m.tech",
    "mtech",
    "master of technology",

    "mca",
    "bca",
    "b.sc",
    "bsc",

    "master",
    "engineering"
]


# ============================================================
# 3. CRITICAL SKILLS
# ============================================================

CRITICAL_SKILLS = [

    # Programming
    "Python",
    "Java",
    "C#",
    "C++",

    # .NET
    ".NET",
    ".NET Core",
    "ASP.NET",
    "ASP.NET Core",
    "Entity Framework",
    "Entity Framework Core",

    # Backend
    "FastAPI",
    "Django",
    "Flask",
    "REST API",

    # Database
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "SQL Server",
    "Oracle",

    # Cloud
    "AWS",
    "GCP",
    "Azure",
    "Azure Functions",
    "Azure API Management",
    "APIM",
    "Azure App Service",

    # AI
    "Machine Learning",
    "Deep Learning",
    "Data Science",
    "Data Analysis",

    # Data Engineering
    "Spark",
    "PySpark",

    # Frontend
    "React",
    "Angular",
    "JavaScript"
]


# ============================================================
# 4. ATS SCORING WEIGHTS
# ============================================================

CRITICAL_SKILL_WEIGHT = 0.45

SUPPORTING_SKILL_WEIGHT = 0.15

SEMANTIC_WEIGHT = 0.15

EXPERIENCE_WEIGHT = 0.15

EDUCATION_WEIGHT = 0.10


# ============================================================
# 5. SUPPORTING SKILL WEIGHTS
# ============================================================

REQUIRED_SKILL_WEIGHT = 0.80

PREFERRED_SKILL_WEIGHT = 0.20


# ============================================================
# 6. EXPERIENCE SETTINGS
# ============================================================

# ============================================================
# EXPERIENCE SETTINGS
# ============================================================

ENTRY_LEVEL_MAX_YEARS = 1.0

ENTRY_LEVEL_INTERNSHIP_SCORE = 100.0

ENTRY_LEVEL_FRESHER_SCORE = 70.0

ENTRY_LEVEL_SOME_EXPERIENCE_SCORE = 90.0

# Minimum internship duration considered relevant
MIN_INTERNSHIP_MONTHS = 3


# ============================================================
# 7. INTERNSHIP KEYWORDS
# ============================================================

INTERNSHIP_KEYWORDS = [

    "intern",
    "internship",

    "software development intern",
    "software engineer intern",
    "software developer intern",

    "python intern",
    "java intern",

    "data analyst intern",
    "data analytics intern",

    "data science intern",

    "machine learning intern",
    "ml intern",

    "ai intern",

    "developer intern",

    "backend intern",

    "frontend intern",

    "web development intern"
]


# ============================================================
# 8. ENTRY LEVEL JOB KEYWORDS
# ============================================================

ENTRY_LEVEL_KEYWORDS = [

    "fresher",
    "freshers",
    "fresh graduate",
    "recent graduate",

    "entry level",
    "entry-level",

    "junior",
    "junior developer",
    "junior python developer",

    "graduate engineer",
    "graduate trainee",
    "trainee",

    "0-1 years",
    "0 - 1 years",
    "0 to 1 years",
    "0–1 years",
    "0 – 1 years",

    "0-1 year",
    "0 - 1 year",
    "0 to 1 year"
]


# ============================================================
# 9. EXPERIENCE DISPLAY
# ============================================================

DISPLAY_EXPERIENCE_IN_MONTHS = True


# ============================================================
# 10. LLM SETTINGS
# ============================================================

LLM_MODEL = "llama-3.3-70b-versatile"

LLM_TEMPERATURE = 0.1

LLM_MAX_TOKENS = 600


# ============================================================
# 11. EMBEDDING MODEL
# ============================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ============================================================
# 12. LLM CANDIDATE LIMIT
# ============================================================

# Only top 5 candidates receive LLM explanations.

LLM_TOP_CANDIDATES = 5


# ============================================================
# 13. PATHS
# ============================================================

JD_FILE = "job_description.txt"

RESUME_FOLDER = "resumes"

OUTPUT_FOLDER = "outputs"