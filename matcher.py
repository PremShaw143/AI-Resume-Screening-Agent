import re

from sklearn.metrics.pairwise import cosine_similarity

from config import (
    REQUIRED_SKILL_WEIGHT,
    PREFERRED_SKILL_WEIGHT,
    CRITICAL_SKILLS
)


# ============================================================
# NORMALIZE SKILL
# ============================================================

def normalize_skill(skill):

    return skill.strip().lower()


# ============================================================
# CHECK SKILL MATCH
# ============================================================

def skill_matches(
    required_skill,
    resume_skills
):

    required = normalize_skill(
        required_skill
    )

    resume_normalized = [

        normalize_skill(skill)

        for skill in resume_skills
    ]

    return required in resume_normalized


# ============================================================
# BASIC SKILL SCORE
# ============================================================

def calculate_skill_scores(
    required_skills,
    preferred_skills,
    resume_skills
):

    # ========================================================
    # REQUIRED SKILLS
    # ========================================================

    required_matched = [

        skill

        for skill in required_skills

        if skill_matches(
            skill,
            resume_skills
        )
    ]


    required_missing = [

        skill

        for skill in required_skills

        if not skill_matches(
            skill,
            resume_skills
        )
    ]


    # ========================================================
    # PREFERRED SKILLS
    # ========================================================

    preferred_matched = [

        skill

        for skill in preferred_skills

        if skill_matches(
            skill,
            resume_skills
        )
    ]


    preferred_missing = [

        skill

        for skill in preferred_skills

        if not skill_matches(
            skill,
            resume_skills
        )
    ]


    # ========================================================
    # REQUIRED SCORE
    # ========================================================

    if required_skills:

        required_score = (

            len(required_matched)

            /

            len(required_skills)

        ) * 100

    else:

        required_score = 100.0


    # ========================================================
    # PREFERRED SCORE
    # ========================================================

    if preferred_skills:

        preferred_score = (

            len(preferred_matched)

            /

            len(preferred_skills)

        ) * 100

    else:

        preferred_score = 100.0


    # ========================================================
    # COMBINED SKILL SCORE
    # ========================================================

    skill_score = (

        required_score
        * REQUIRED_SKILL_WEIGHT

        +

        preferred_score
        * PREFERRED_SKILL_WEIGHT
    )


    return {

        "skill_score":
            float(skill_score),

        "required_score":
            float(required_score),

        "preferred_score":
            float(preferred_score),

        "required_matched":
            required_matched,

        "required_missing":
            required_missing,

        "preferred_matched":
            preferred_matched,

        "preferred_missing":
            preferred_missing
    }


# ============================================================
# CRITICAL SKILL SCORE
# ============================================================
#
# This focuses on the technologies that are central to the
# job.
#
# Example Azure .NET JD:
#
# C#
# .NET Core
# Azure Functions
# APIM
# SQL Server
#
# Missing these skills should significantly affect the score.
#
# ============================================================

def calculate_critical_skill_score(
    required_skills,
    resume_skills
):

    # --------------------------------------------------------
    # Find critical skills actually required by the JD
    # --------------------------------------------------------

    critical_required = [

        skill

        for skill in required_skills

        if any(

            normalize_skill(skill)
            ==
            normalize_skill(critical)

            for critical in CRITICAL_SKILLS
        )
    ]


    # --------------------------------------------------------
    # If JD has no critical skills
    # --------------------------------------------------------

    if not critical_required:

        return {

            "critical_score": 100.0,

            "critical_required":
                [],

            "critical_matched":
                [],

            "critical_missing":
                []
        }


    # --------------------------------------------------------
    # Match critical skills
    # --------------------------------------------------------

    critical_matched = [

        skill

        for skill in critical_required

        if skill_matches(
            skill,
            resume_skills
        )
    ]


    critical_missing = [

        skill

        for skill in critical_required

        if not skill_matches(
            skill,
            resume_skills
        )
    ]


    # --------------------------------------------------------
    # Score
    # --------------------------------------------------------

    critical_score = (

        len(critical_matched)

        /

        len(critical_required)

    ) * 100


    return {

        "critical_score":
            float(critical_score),

        "critical_required":
            critical_required,

        "critical_matched":
            critical_matched,

        "critical_missing":
            critical_missing
    }


# ============================================================
# SUPPORTING SKILL SCORE
# ============================================================
#
# Supporting score includes:
#
# - Required skills that are NOT critical
# - Preferred skills
#
# ============================================================

def calculate_supporting_skill_score(
    required_skills,
    preferred_skills,
    resume_skills,
    critical_result
):

    critical_required = (
        critical_result[
            "critical_required"
        ]
    )


    # ========================================================
    # NON-CRITICAL REQUIRED SKILLS
    # ========================================================

    supporting_required = [

        skill

        for skill in required_skills

        if skill not in critical_required
    ]


    supporting_required_matched = [

        skill

        for skill in supporting_required

        if skill_matches(
            skill,
            resume_skills
        )
    ]


    supporting_required_missing = [

        skill

        for skill in supporting_required

        if not skill_matches(
            skill,
            resume_skills
        )
    ]


    # ========================================================
    # PREFERRED SKILLS
    # ========================================================

    preferred_matched = [

        skill

        for skill in preferred_skills

        if skill_matches(
            skill,
            resume_skills
        )
    ]


    preferred_missing = [

        skill

        for skill in preferred_skills

        if not skill_matches(
            skill,
            resume_skills
        )
    ]


    # ========================================================
    # REQUIRED SUPPORTING SCORE
    # ========================================================

    if supporting_required:

        supporting_required_score = (

            len(
                supporting_required_matched
            )

            /

            len(
                supporting_required
            )

        ) * 100

    else:

        supporting_required_score = 100.0


    # ========================================================
    # PREFERRED SCORE
    # ========================================================

    if preferred_skills:

        preferred_score = (

            len(
                preferred_matched
            )

            /

            len(
                preferred_skills
            )

        ) * 100

    else:

        preferred_score = 100.0


    # ========================================================
    # SUPPORTING SCORE
    # ========================================================

    supporting_score = (

        supporting_required_score
        * 0.70

        +

        preferred_score
        * 0.30
    )


    return {

        "supporting_score":
            float(supporting_score),

        "supporting_required":
            supporting_required,

        "supporting_required_matched":
            supporting_required_matched,

        "supporting_required_missing":
            supporting_required_missing,

        "preferred_matched":
            preferred_matched,

        "preferred_missing":
            preferred_missing,

        "supporting_required_score":
            float(
                supporting_required_score
            ),

        "preferred_score":
            float(
                preferred_score
            )
    }


# ============================================================
# SEMANTIC SIMILARITY
# ============================================================

def calculate_semantic_similarity(
    model,
    jd,
    resume
):

    if not jd or not resume:

        return 0.0


    # --------------------------------------------------------
    # Create embeddings
    # --------------------------------------------------------

    jd_embedding = model.encode(
        jd
    )


    resume_embedding = model.encode(
        resume
    )


    # --------------------------------------------------------
    # Cosine similarity
    # --------------------------------------------------------

    similarity = cosine_similarity(

        [jd_embedding],

        [resume_embedding]

    )[0][0]


    # --------------------------------------------------------
    # Convert to percentage
    # --------------------------------------------------------

    score = max(

        0,

        similarity * 100

    )


    return float(
        round(
            score,
            2
        )
    )