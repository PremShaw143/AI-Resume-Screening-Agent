import os
import json
import time

from dotenv import load_dotenv
from groq import Groq

from config import (
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    INTERNSHIP_KEYWORDS,
    ENTRY_LEVEL_KEYWORDS
)


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv(
    "GROQ_API_KEY"
)

if not api_key:

    raise ValueError(
        "GROQ_API_KEY not found. "
        "Please add it to your .env file."
    )


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=api_key
)


# ============================================================
# FORMAT EXPERIENCE
# ============================================================

def format_experience(
    experience_years
):

    try:

        years = float(
            experience_years
        )

    except (
        ValueError,
        TypeError
    ):

        return "Experience not detected"

    if years <= 0:

        return "No experience"

    months = round(
        years * 12
    )

    if months < 12:

        if months == 1:

            return "1 month"

        return f"{months} months"

    whole_years = months // 12

    remaining_months = (
        months % 12
    )

    if remaining_months == 0:

        if whole_years == 1:

            return "1 year"

        return f"{whole_years} years"

    year_text = (
        "year"
        if whole_years == 1
        else "years"
    )

    month_text = (
        "month"
        if remaining_months == 1
        else "months"
    )

    return (
        f"{whole_years} {year_text} "
        f"{remaining_months} {month_text}"
    )


# ============================================================
# DETECT ENTRY LEVEL ROLE
# ============================================================

def is_entry_level_role(
    jd
):

    if not jd:

        return False

    jd_lower = jd.lower()

    return any(

        keyword.lower()
        in jd_lower

        for keyword
        in ENTRY_LEVEL_KEYWORDS
    )


# ============================================================
# DETECT INTERNSHIP
# ============================================================

def has_internship(
    resume_text
):

    if not resume_text:

        return False

    resume_lower = (
        resume_text.lower()
    )

    return any(

        keyword.lower()
        in resume_lower

        for keyword
        in INTERNSHIP_KEYWORDS
    )


# ============================================================
# REMOVE EXPERIENCE GAPS
# ============================================================

def remove_experience_gaps(
    gaps
):

    if not gaps:

        return []

    experience_words = [

        "limited experience",
        "limited work experience",
        "limited professional experience",
        "insufficient experience",
        "lack of professional experience",
        "lacks professional experience",
        "not enough experience",
        "insufficient work experience",
        "limited industry experience",
        "limited industry exposure",
        "only 3 months",
        "only 0.25 years",
        "only 0.5 years"
    ]

    cleaned = []

    for gap in gaps:

        gap_text = str(
            gap
        )

        gap_lower = (
            gap_text.lower()
        )

        is_experience_gap = any(

            word in gap_lower

            for word
            in experience_words
        )

        if not is_experience_gap:

            cleaned.append(
                gap_text
            )

    return cleaned


# ============================================================
# REMOVE DUPLICATE GAPS
# ============================================================

def remove_duplicate_items(
    items
):

    if not items:

        return []

    cleaned = []

    seen = set()

    for item in items:

        item = str(
            item
        ).strip()

        normalized = (
            item.lower()
        )

        if normalized in seen:

            continue

        seen.add(
            normalized
        )

        cleaned.append(
            item
        )

    return cleaned


# ============================================================
# GENERATE LLM EXPLANATION
# ============================================================

def generate_llm_explanation(
    jd,
    result,
    resume_text
):

    # ========================================================
    # EXPERIENCE
    # ========================================================

    experience_years = result.get(
        "experience_years",
        0
    )

    experience_display = (
        format_experience(
            experience_years
        )
    )

    experience_score = float(
        result.get(
            "experience_score",
            0
        )
    )

    entry_level = (
        is_entry_level_role(
            jd
        )
    )

    internship = (
        has_internship(
            resume_text
        )
    )

    # ========================================================
    # NEW ATS SCORE FIELDS
    # ========================================================

    final_score = float(
        result.get(
            "final_score",
            0
        )
    )

    critical_score = float(
        result.get(
            "critical_score",
            0
        )
    )

    supporting_score = float(
        result.get(
            "supporting_score",
            0
        )
    )

    semantic_score = float(
        result.get(
            "semantic_score",
            0
        )
    )

    education_score = float(
        result.get(
            "education_score",
            0
        )
    )

    # ========================================================
    # CRITICAL SKILLS
    # ========================================================

    critical_required = result.get(
        "critical_required",
        []
    )

    critical_matched = result.get(
        "critical_matched",
        []
    )

    critical_missing = result.get(
        "critical_missing",
        []
    )

    # ========================================================
    # SUPPORTING SKILLS
    # ========================================================

    supporting_required = result.get(
        "supporting_required",
        []
    )

    supporting_matched = result.get(
        "supporting_required_matched",
        []
    )

    supporting_missing = result.get(
        "supporting_required_missing",
        []
    )

    # ========================================================
    # PREFERRED SKILLS
    # ========================================================

    preferred_matched = result.get(
        "preferred_matched",
        []
    )

    preferred_missing = result.get(
        "preferred_missing",
        []
    )

    # ========================================================
    # EDUCATION
    # ========================================================

    education = result.get(
        "education",
        []
    )

    # ========================================================
    # EXPERIENCE RULE
    # ========================================================

    internship_is_strength = (

        entry_level

        and

        internship

        and

        experience_score >= 100
    )

    if internship_is_strength:

        experience_instruction = f"""

The candidate has {experience_display}
of relevant internship experience.

This is an entry-level / 0–1 year role.

The Python ATS calculated an Experience Score
of 100%.

Therefore:

- Treat the internship as a STRENGTH.
- Mention the internship positively.
- Do NOT describe the candidate as having limited experience.
- Do NOT put internship duration in GAPS.
- Do NOT say "only 3 months".
- Do NOT say "only 0.25 years".
- Do NOT say "limited work experience".
- Do NOT say "insufficient experience".
- Do NOT say "lack of professional experience".
"""

    elif entry_level:

        experience_instruction = """

This is an entry-level role.

Do not unnecessarily penalize the candidate
for having less than one year of experience.

If relevant internship experience exists,
mention it positively.

Only mention experience as a gap if the
candidate clearly fails an explicit
experience requirement.
"""

    else:

        experience_instruction = """

Evaluate the candidate's experience against
the Job Description.

Only mention insufficient experience as a gap
when the candidate clearly has less experience
than the explicit requirement.

Do not invent experience.
"""

    # ========================================================
    # PROMPT
    # ========================================================

    prompt = f"""

You are an AI Resume Screening Assistant.

Your job is to explain the screening result
for a candidate.

The Python ATS scoring engine has already
calculated the score.

You MUST NOT change the score.

You are only explaining the result.

============================================================
GENERAL RULES
============================================================

1. Do not change the calculated score.

2. Do not invent candidate information.

3. Use only the provided resume, JD,
   and screening data.

4. Mention genuine strengths.

5. Mention genuine gaps.

6. Do not claim a skill exists if it is
   not present in the screening data
   or resume.

7. Do not treat transferable skills as
   exact technology matches.

8. Do not claim Python is equivalent to C#.

9. Do not claim FastAPI is equivalent
   to ASP.NET Core.

10. Do not claim MySQL is equivalent
    to SQL Server.

11. Do not claim Docker is equivalent
    to Azure.

12. If a critical JD technology is missing,
    clearly mention it as a gap.

13. Do not repeat the same gap.

14. Keep the explanation concise.

15. Do not claim professional experience
    if the resume only shows internships.

============================================================
SCORING ARCHITECTURE
============================================================

Critical Skills = 40%

Supporting Skills = 15%

Semantic Similarity = 15%

Experience = 20%

Education = 10%

The final score is calculated by the Python
screening engine.

============================================================
EXPERIENCE RULE
============================================================

{experience_instruction}

============================================================
JOB DESCRIPTION
============================================================

{jd}

============================================================
CANDIDATE
============================================================

{result.get("candidate", "Unknown")}

============================================================
SCREENING RESULTS
============================================================

Final Score:
{final_score}%

Decision:
{result.get("decision", "")}

Critical Skill Score:
{critical_score}%

Supporting Skill Score:
{supporting_score}%

Semantic Similarity:
{semantic_score}%

Experience Score:
{experience_score}%

Education Score:
{education_score}%

Candidate Experience:
{experience_display}

Internship Detected:
{"Yes" if internship else "No"}

Entry-Level Role:
{"Yes" if entry_level else "No"}

============================================================
CRITICAL SKILLS REQUIRED
============================================================

{", ".join(critical_required) if critical_required else "None"}

============================================================
CRITICAL SKILLS MATCHED
============================================================

{", ".join(critical_matched) if critical_matched else "None"}

============================================================
CRITICAL SKILLS MISSING
============================================================

{", ".join(critical_missing) if critical_missing else "None"}

============================================================
SUPPORTING REQUIRED SKILLS
============================================================

{", ".join(supporting_required) if supporting_required else "None"}

============================================================
SUPPORTING SKILLS MATCHED
============================================================

{", ".join(supporting_matched) if supporting_matched else "None"}

============================================================
SUPPORTING SKILLS MISSING
============================================================

{", ".join(supporting_missing) if supporting_missing else "None"}

============================================================
PREFERRED SKILLS MATCHED
============================================================

{", ".join(preferred_matched) if preferred_matched else "None"}

============================================================
PREFERRED SKILLS MISSING
============================================================

{", ".join(preferred_missing) if preferred_missing else "None"}

============================================================
EDUCATION
============================================================

{", ".join(education) if education else "None detected"}

============================================================
RESUME
============================================================

{resume_text}

============================================================
OUTPUT
============================================================

Return ONLY valid JSON.

Do not use Markdown.

Use exactly:

{{
    "summary": "Short explanation of overall candidate fit.",

    "strengths": [
        "strength 1",
        "strength 2",
        "strength 3"
    ],

    "gaps": [
        "gap 1",
        "gap 2"
    ],

    "recommendation": "Short hiring recommendation."
}}

============================================================
FINAL RULES
============================================================

If the candidate is an entry-level / 0–1 year
candidate and has a relevant internship with
Experience Score = 100%:

The internship MUST appear as a strength.

The internship MUST NOT appear as a gap.

Never say:

"Limited experience"

"Limited work experience"

"Only 3 months"

"Only 0.25 years"

"Insufficient experience"

"Lack of professional experience"

If critical skills are missing, mention the
actual missing technologies.

For example:

If the JD requires:

C#
.NET Core
Azure Functions
Azure API Management
SQL Server

and the candidate only has:

Python
FastAPI
MySQL

then clearly identify the missing C#/.NET/Azure
technologies rather than calling the candidate
a strong .NET match.
"""

    # ========================================================
    # GROQ API WITH RETRY
    # ========================================================

    last_error = None

    for attempt in range(3):

        try:

            response = client.chat.completions.create(

                model=LLM_MODEL,

                messages=[

                    {
                        "role": "system",

                        "content": (
                            "You are a precise recruitment "
                            "screening assistant. "
                            "Follow the Python ATS results "
                            "exactly. "
                            "Never invent information. "
                            "Return valid JSON only."
                        )
                    },

                    {
                        "role": "user",

                        "content": prompt
                    }
                ],

                temperature=LLM_TEMPERATURE,

                max_tokens=LLM_MAX_TOKENS
            )

            # =================================================
            # GET RESPONSE
            # =================================================

            output = (
                response
                .choices[0]
                .message
                .content
                .strip()
            )

            # =================================================
            # REMOVE MARKDOWN
            # =================================================

            if output.startswith(
                "```"
            ):

                output = output.replace(
                    "```json",
                    ""
                )

                output = output.replace(
                    "```",
                    ""
                )

                output = output.strip()

            # =================================================
            # PARSE JSON
            # =================================================

            result_json = json.loads(
                output
            )

            if not isinstance(
                result_json,
                dict
            ):

                raise ValueError(
                    "Invalid JSON structure"
                )

            # =================================================
            # DEFAULT FIELDS
            # =================================================

            result_json.setdefault(
                "summary",
                ""
            )

            result_json.setdefault(
                "strengths",
                []
            )

            result_json.setdefault(
                "gaps",
                []
            )

            result_json.setdefault(
                "recommendation",
                ""
            )

            # =================================================
            # CLEAN EXPERIENCE GAPS
            # =================================================

            if internship_is_strength:

                result_json["gaps"] = (
                    remove_experience_gaps(
                        result_json[
                            "gaps"
                        ]
                    )
                )

                # ---------------------------------------------
                # Ensure internship is strength
                # ---------------------------------------------

                internship_already_strength = any(

                    "intern" in str(
                        strength
                    ).lower()

                    for strength
                    in result_json[
                        "strengths"
                    ]
                )

                if not internship_already_strength:

                    result_json[
                        "strengths"
                    ].insert(

                        0,

                        (
                            "Relevant internship experience "
                            "providing practical industry "
                            "exposure"
                        )
                    )

            # =================================================
            # REMOVE DUPLICATES
            # =================================================

            result_json["strengths"] = (
                remove_duplicate_items(
                    result_json[
                        "strengths"
                    ]
                )
            )

            result_json["gaps"] = (
                remove_duplicate_items(
                    result_json[
                        "gaps"
                    ]
                )
            )

            # =================================================
            # LIMIT OUTPUT
            # =================================================

            result_json["strengths"] = [

                str(item)

                for item
                in result_json[
                    "strengths"
                ][:5]
            ]

            result_json["gaps"] = [

                str(item)

                for item
                in result_json[
                    "gaps"
                ][:4]
            ]

            return result_json

        except Exception as error:

            last_error = error

            print(
                f"LLM attempt "
                f"{attempt + 1}/3 failed: "
                f"{error}"
            )

            if attempt < 2:

                time.sleep(2)

    # ========================================================
    # FALLBACK
    # ========================================================

    return {

        "summary":
            "AI explanation could not be generated.",

        "strengths": [],

        "gaps": [],

        "recommendation":
            "Review the calculated screening results manually.",

        "error":
            str(last_error)
    }