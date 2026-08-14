def generate_explanation(result):

    strengths = []
    gaps = []

    # ========================================================
    # SKILL STRENGTHS
    # ========================================================

    if result["required_matched"]:

        strengths.append(
            "Strong match with required skills: "
            + ", ".join(result["required_matched"])
        )

    if result["preferred_matched"]:

        strengths.append(
            "Additional preferred skills: "
            + ", ".join(result["preferred_matched"])
        )

    # ========================================================
    # EXPERIENCE
    # ========================================================

    experience = result.get(
        "experience_years",
        0
    )

    # --------------------------------------------------------
    # Internship / entry-level experience
    # --------------------------------------------------------

    if experience > 0:

        strengths.append(
            "Relevant internship experience demonstrates "
            "practical exposure to the field"
        )

    # --------------------------------------------------------
    # DO NOT add limited-experience gap for junior roles
    # --------------------------------------------------------

    # No:
    # gaps.append(
    #     f"Limited experience ({experience} years)"
    # )

    # ========================================================
    # MISSING REQUIRED SKILLS
    # ========================================================

    if result["required_missing"]:

        gaps.append(
            "Missing required skills: "
            + ", ".join(
                result["required_missing"]
            )
        )

    # ========================================================
    # MISSING PREFERRED SKILLS
    # ========================================================

    if result["preferred_missing"]:

        gaps.append(
            "Missing preferred skills: "
            + ", ".join(
                result["preferred_missing"]
            )
        )

    # ========================================================
    # RECOMMENDATION
    # ========================================================

    if result["final_score"] >= 80:

        recommendation = (
            "Strong candidate. "
            "Proceed to the next stage of the hiring process."
        )

    elif result["final_score"] >= 65:

        recommendation = (
            "Good candidate. "
            "Proceed with an interview or technical assessment."
        )

    elif result["final_score"] >= 50:

        recommendation = (
            "Consider the candidate for further evaluation."
        )

    else:

        recommendation = (
            "Candidate requires further review."
        )

    return {

        "candidate":
            result["candidate"],

        "score":
            result["final_score"],

        "decision":
            result["decision"],

        "strengths":
            strengths,

        "gaps":
            gaps,

        "recommendation":
            recommendation
    }