import re
import pymupdf

from config import (
    SKILLS,
    EDUCATION_KEYWORDS
)


# ============================================================
# SKILL ALIASES
# ============================================================
# Different ways a skill may appear in a resume/JD.
# All aliases are converted to one standard skill name.
# ============================================================

SKILL_ALIASES = {

    "REST API": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
        "rest-api",
        "restful-api"
    ],

    "FastAPI": [
        "fastapi",
        "fast api"
    ],

    "Scikit-Learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn"
    ],

    "Machine Learning": [
        "machine learning",
        "machine-learning"
    ],

    "Deep Learning": [
        "deep learning",
        "deep-learning"
    ],

    "Data Science": [
        "data science",
        "data-science"
    ],

    "Data Analysis": [
        "data analysis",
        "data analytics"
    ],

    "Power BI": [
        "power bi",
        "powerbi"
    ],

    "C++": [
        "c++",
        "cpp"
    ],

    "GitHub": [
        "github",
        "git hub"
    ],

    "MySQL": [
        "mysql",
        "my sql"
    ],

    "PostgreSQL": [
        "postgresql",
        "postgres"
    ],

    "MongoDB": [
        "mongodb",
        "mongo db"
    ],

    "PySpark": [
        "pyspark",
        "py spark"
    ],

    "JavaScript": [
        "javascript",
        "java script"
    ],

    "Data Structures": [
        "data structures",
        "data structure"
    ]
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    if not text:

        return ""

    text = text.lower()

    # Normalize different dash characters
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Normalize multiple spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# PDF EXTRACTION
# ============================================================

def extract_pdf_text(file_path):

    doc = pymupdf.open(file_path)

    text = ""

    try:

        for page in doc:

            text += page.get_text()

    finally:

        doc.close()

    return text


# ============================================================
# JOB DESCRIPTION
# ============================================================

def load_job_description(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ============================================================
# CHECK PHRASE IN TEXT
# ============================================================

def contains_phrase(
    text,
    phrase
):

    text = normalize_text(text)

    phrase = normalize_text(phrase)

    # Escape special regex characters
    pattern = (
        r"(?<!\w)"
        + re.escape(phrase)
        + r"(?!\w)"
    )

    return bool(
        re.search(
            pattern,
            text
        )
    )


# ============================================================
# FIND CANONICAL SKILL
# ============================================================

def find_skill_match(
    text,
    skill
):

    # --------------------------------------------------------
    # Check aliases first
    # --------------------------------------------------------

    if skill in SKILL_ALIASES:

        aliases = SKILL_ALIASES[skill]

        for alias in aliases:

            if contains_phrase(
                text,
                alias
            ):

                return True

        return False


    # --------------------------------------------------------
    # Normal skill matching
    # --------------------------------------------------------

    return contains_phrase(
        text,
        skill
    )


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(text):

    if not text:

        return []


    found_skills = []


    # --------------------------------------------------------
    # Check every canonical skill
    # --------------------------------------------------------

    for skill in SKILLS:

        if find_skill_match(
            text,
            skill
        ):

            found_skills.append(
                skill
            )


    # --------------------------------------------------------
    # Add alias-based skills that may not be present
    # directly in SKILLS
    # --------------------------------------------------------

    for canonical_skill, aliases in SKILL_ALIASES.items():

        if canonical_skill in found_skills:

            continue


        for alias in aliases:

            if contains_phrase(
                text,
                alias
            ):

                found_skills.append(
                    canonical_skill
                )

                break


    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    found_skills = list(
        dict.fromkeys(
            found_skills
        )
    )


    return found_skills


# ============================================================
# SECTION EXTRACTION
# ============================================================

def extract_section(
    text,
    start_marker,
    end_markers
):

    text_lower = text.lower()

    start_marker = start_marker.lower()

    start = text_lower.find(
        start_marker
    )

    if start == -1:

        return ""


    start += len(
        start_marker
    )


    end_positions = []


    for marker in end_markers:

        position = text_lower.find(
            marker.lower(),
            start
        )

        if position != -1:

            end_positions.append(
                position
            )


    if end_positions:

        end = min(
            end_positions
        )

        return text[start:end]


    return text[start:]


# ============================================================
# REQUIRED SKILLS
# ============================================================

def extract_required_skills(jd):

    section = extract_section(

        jd,

        "REQUIRED SKILLS:",

        [
            "PREFERRED SKILLS:",
            "EDUCATION:",
            "EXPERIENCE:",
            "RESPONSIBILITIES:",
            "JOB RESPONSIBILITIES:"
        ]
    )


    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------
    # If the JD doesn't have a REQUIRED SKILLS section,
    # extract skills from the complete JD.
    # --------------------------------------------------------

    if not section.strip():

        return extract_skills(jd)


    return extract_skills(
        section
    )


# ============================================================
# PREFERRED SKILLS
# ============================================================

def extract_preferred_skills(jd):

    section = extract_section(

        jd,

        "PREFERRED SKILLS:",

        [
            "EDUCATION:",
            "EXPERIENCE:",
            "RESPONSIBILITIES:",
            "JOB RESPONSIBILITIES:"
        ]
    )


    if not section.strip():

        return []


    return extract_skills(
        section
    )


# ============================================================
# EXPERIENCE EXTRACTION
# ============================================================

 # ============================================================
# EXPERIENCE EXTRACTION
# ============================================================

def extract_experience(text):

    text = normalize_text(text)

    # --------------------------------------------------------
    # 1. Explicit years of experience
    #
    # Examples:
    # 2 years experience
    # 1.5 years of experience
    # 3+ years professional experience
    # --------------------------------------------------------

    year_patterns = [

        r"(\d+(?:\.\d+)?)\+?\s*years?"
        r"\s+(?:of\s+)?experience",

        r"(\d+(?:\.\d+)?)\+?\s*years?"
        r"\s+(?:of\s+)?professional\s+experience",

        r"(\d+(?:\.\d+)?)\+?\s*years?"
        r"\s+(?:of\s+)?work\s+experience"
    ]


    for pattern in year_patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            try:

                return float(
                    match.group(1)
                )

            except ValueError:

                pass


    # --------------------------------------------------------
    # 2. Explicit months of experience
    #
    # Examples:
    # 6 months experience
    # 8 months of experience
    # 3 months professional experience
    # --------------------------------------------------------

    month_patterns = [

        r"(\d+)\+?\s*months?"
        r"\s+(?:of\s+)?experience",

        r"(\d+)\+?\s*months?"
        r"\s+(?:of\s+)?professional\s+experience"
    ]


    for pattern in month_patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            try:

                months = float(
                    match.group(1)
                )

                return months / 12

            except ValueError:

                pass


    # --------------------------------------------------------
    # 3. Internship duration
    #
    # Examples:
    # 6-month internship
    # 6 month internship
    # 3 months internship
    # --------------------------------------------------------

    internship_patterns = [

        r"(\d+)\s*-\s*month\s+internship",

        r"(\d+)\s*month\s+internship",

        r"(\d+)\s*months\s+internship"
    ]


    for pattern in internship_patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            try:

                months = float(
                    match.group(1)
                )

                return months / 12

            except ValueError:

                pass


    # --------------------------------------------------------
    # 4. Internship mentioned but duration unknown
    #
    # IMPORTANT:
    # Don't automatically assume 0.5 years.
    # --------------------------------------------------------

    if (
        "internship" in text
        or "intern" in text
    ):

        return 0.25


    # --------------------------------------------------------
    # 5. Fresher / recent graduate
    # --------------------------------------------------------

    if (
        "fresher" in text
        or "fresh graduate" in text
        or "recent graduate" in text
    ):

        return 0.0


    # --------------------------------------------------------
    # 6. Nothing detected
    # --------------------------------------------------------

    return 0.0

    # --------------------------------------------------------
    # Internship
    # --------------------------------------------------------

    if (
        "intern" in text
        or "internship" in text
    ):

        return 0.5


    # --------------------------------------------------------
    # Fresher
    # --------------------------------------------------------

    if (
        "fresher" in text
        or "fresh graduate" in text
        or "recent graduate" in text
    ):

        return 0.0


    return 0.0


# ============================================================
# EDUCATION EXTRACTION
# ============================================================

def extract_education(text):

    text = normalize_text(
        text
    )


    found = []


    for keyword in EDUCATION_KEYWORDS:

        keyword = normalize_text(
            keyword
        )

        if keyword in text:

            found.append(
                keyword
            )


    return list(
        dict.fromkeys(
            found
        )
    )