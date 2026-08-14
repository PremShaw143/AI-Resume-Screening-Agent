import re

from extractor import extract_experience

from config import (
    ENTRY_LEVEL_MAX_YEARS,
    ENTRY_LEVEL_INTERNSHIP_SCORE,
    ENTRY_LEVEL_FRESHER_SCORE,
    ENTRY_LEVEL_SOME_EXPERIENCE_SCORE,
    MIN_INTERNSHIP_MONTHS,
    INTERNSHIP_KEYWORDS,
    ENTRY_LEVEL_KEYWORDS
)


# ============================================================
# 1. EXTRACT REQUIRED EXPERIENCE
# ============================================================

def extract_required_experience(jd_text):

    if not jd_text:

        return (
            0.0,
            0.0
        )

    jd_text = jd_text.lower()

    # --------------------------------------------------------
    # Ranges
    # --------------------------------------------------------

    range_patterns = [

        r"(\d+(?:\.\d+)?)\s*[-–]\s*"
        r"(\d+(?:\.\d+)?)\s*years?",

        r"(\d+(?:\.\d+)?)\s+to\s+"
        r"(\d+(?:\.\d+)?)\s*years?"
    ]

    for pattern in range_patterns:

        match = re.search(
            pattern,
            jd_text
        )

        if match:

            try:

                return (
                    float(match.group(1)),
                    float(match.group(2))
                )

            except ValueError:

                pass

    # --------------------------------------------------------
    # Single requirement
    # --------------------------------------------------------

    patterns = [

        r"(\d+(?:\.\d+)?)\+?\s*years?"
        r"\s+(?:of\s+)?experience",

        r"(\d+(?:\.\d+)?)\+?\s*years?"
        r"\s+(?:of\s+)?professional\s+experience",

        r"(\d+(?:\.\d+)?)\+?\s*years?"
        r"\s+(?:of\s+)?work\s+experience"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            jd_text
        )

        if match:

            try:

                experience = float(
                    match.group(1)
                )

                return (
                    experience,
                    experience
                )

            except ValueError:

                pass

    # --------------------------------------------------------
    # Entry level
    # --------------------------------------------------------

    if any(
        keyword in jd_text
        for keyword in ENTRY_LEVEL_KEYWORDS
    ):

        return (
            0.0,
            ENTRY_LEVEL_MAX_YEARS
        )

    return (
        0.0,
        0.0
    )


# ============================================================
# 2. INTERNSHIP DETECTION
# ============================================================

def has_internship_experience(
    resume_text
):

    if not resume_text:

        return False

    text = resume_text.lower()

    return any(

        keyword.lower() in text

        for keyword in INTERNSHIP_KEYWORDS
    )


# ============================================================
# 3. EXPERIENCE SCORE
# ============================================================

def calculate_experience_score(
    resume_text,
    jd_text
):

    candidate_experience = extract_experience(
        resume_text
    )

    (
        minimum_experience,
        maximum_experience
    ) = extract_required_experience(
        jd_text
    )

    internship = has_internship_experience(
        resume_text
    )

    # ========================================================
    # ENTRY LEVEL / 0-1 YEAR
    # ========================================================

    if (
        maximum_experience > 0
        and
        maximum_experience <=
        ENTRY_LEVEL_MAX_YEARS
    ):

        # ----------------------------------------------------
        # 3+ month internship
        # ----------------------------------------------------

        if (
            internship
            and
            candidate_experience
            >= (
                MIN_INTERNSHIP_MONTHS
                / 12
            )
        ):

            return (
                ENTRY_LEVEL_INTERNSHIP_SCORE,
                candidate_experience
            )

        # ----------------------------------------------------
        # Any other experience
        # ----------------------------------------------------

        if candidate_experience > 0:

            return (
                ENTRY_LEVEL_SOME_EXPERIENCE_SCORE,
                candidate_experience
            )

        # ----------------------------------------------------
        # True fresher
        # ----------------------------------------------------

        return (
            ENTRY_LEVEL_FRESHER_SCORE,
            candidate_experience
        )

    # ========================================================
    # NO EXPERIENCE REQUIREMENT IN JD
    # ========================================================

    if (
        minimum_experience == 0
        and
        maximum_experience == 0
    ):

        if candidate_experience > 0:

            return (
                100.0,
                candidate_experience
            )

        if internship:

            return (
                100.0,
                candidate_experience
            )

        return (
            70.0,
            candidate_experience
        )

    # ========================================================
    # CANDIDATE MEETS MINIMUM
    # ========================================================

    if (
        candidate_experience
        >= minimum_experience
    ):

        return (
            100.0,
            candidate_experience
        )

    # ========================================================
    # BELOW MINIMUM
    # ========================================================

    if (
        candidate_experience > 0
        and
        minimum_experience > 0
    ):

        score = (

            candidate_experience
            /
            minimum_experience

        ) * 100

        return (
            min(
                score,
                100.0
            ),
            candidate_experience
        )

    return (
        0.0,
        candidate_experience
    )


# ============================================================
# 4. FORMAT EXPERIENCE
# ============================================================

def format_experience(years):

    if years is None:

        return "Not detected"

    try:

        years = float(years)

    except (
        ValueError,
        TypeError
    ):

        return "Not detected"

    if years <= 0:

        return "No experience"

    if years < 1:

        months = round(
            years * 12
        )

        if months <= 1:

            return "1 month"

        return f"{months} months"

    if years.is_integer():

        count = int(years)

        if count == 1:

            return "1 year"

        return f"{count} years"

    whole_years = int(years)

    months = round(
        (years - whole_years) * 12
    )

    if months == 12:

        whole_years += 1
        months = 0

    if months == 0:

        if whole_years == 1:

            return "1 year"

        return f"{whole_years} years"

    if whole_years == 0:

        return (
            f"{months} "
            f"{'month' if months == 1 else 'months'}"
        )

    return (
        f"{whole_years} "
        f"{'year' if whole_years == 1 else 'years'} "
        f"{months} "
        f"{'month' if months == 1 else 'months'}"
    )
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
# 5. EDUCATION SCORE
# ============================================================

def calculate_education_score(
    resume_text,
    jd_text
):

    resume_text = (
        resume_text.lower()
        if resume_text
        else ""
    )

    relevant_degrees = [

        "b.tech",
        "btech",
        "b.e.",
        "be ",
        "bachelor of technology",
        "bachelor's",
        "bachelor",

        "m.tech",
        "mtech",
        "master of technology",

        "mca",
        "bca",

        "b.sc",
        "bsc",

        "master"
    ]

    candidate_has_degree = any(

        degree in resume_text

        for degree in relevant_degrees
    )

    if not candidate_has_degree:

        return (
            0.0,
            []
        )

    education_keywords = [

        "computer science",
        "data science",
        "information technology",
        "software engineering",
        "computer engineering",
        "artificial intelligence",
        "machine learning",
        "information systems",
        "computer applications"
    ]

    found_education = []

    for keyword in education_keywords:

        if keyword in resume_text:

            found_education.append(
                keyword
            )

    found_education = list(
        dict.fromkeys(
            found_education
        )
    )

    if found_education:

        return (
            100.0,
            found_education
        )

    return (
        70.0,
        []
    )


# ============================================================
# 6. FINAL ATS SCORE
# ============================================================

def calculate_final_score(
    critical_skill_score,
    supporting_skill_score,
    semantic_score,
    education_score,
    experience_score
):

    final_score = (

        critical_skill_score * 0.40

        +

        supporting_skill_score * 0.15

        +

        semantic_score * 0.15

        +

        experience_score * 0.20

        +

        education_score * 0.10
    )

    final_score = max(
        0.0,
        min(
            final_score,
            100.0
        )
    )

    return float(
        round(
            final_score,
            2
        )
    )


# ============================================================
# 7. DECISION
# ============================================================

def get_decision(
    final_score
):

    if final_score >= 80:

        return "Strong Match"

    elif final_score >= 65:

        return "Good Match"

    elif final_score >= 50:

        return "Moderate Match"

    return "Weak Match"