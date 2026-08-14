import os

from sentence_transformers import SentenceTransformer

from config import (
    JD_FILE,
    RESUME_FOLDER,
    OUTPUT_FOLDER,
    EMBEDDING_MODEL,
    LLM_TOP_CANDIDATES
)

from extractor import (
    load_job_description,
    extract_pdf_text,
    extract_required_skills,
    extract_preferred_skills,
    extract_skills
)

from matcher import (
    calculate_skill_scores,
    calculate_critical_skill_score,
    calculate_supporting_skill_score,
    calculate_semantic_similarity
)

from scorer import (
    calculate_experience_score,
    calculate_education_score,
    calculate_final_score,
    get_decision
)

from reporter import (
    display_results,
    save_csv,
    save_json
)

from explainer import (
    generate_explanation
)

from llm_explainer import (
    generate_llm_explanation
)


# ============================================================
# 1. LOAD JOB DESCRIPTION
# ============================================================

print("\nLoading Job Description...")

jd = load_job_description(
    JD_FILE
)

print(
    "Job Description loaded successfully."
)


# ============================================================
# 2. EXTRACT JOB REQUIREMENTS
# ============================================================

required_skills = extract_required_skills(
    jd
)

preferred_skills = extract_preferred_skills(
    jd
)


print("\n" + "=" * 90)
print("JOB REQUIREMENTS")
print("=" * 90)

print("\nRequired Skills:")

print(
    ", ".join(required_skills)
    if required_skills
    else "None detected"
)

print("\nPreferred Skills:")

print(
    ", ".join(preferred_skills)
    if preferred_skills
    else "None detected"
)


# ============================================================
# 3. LOAD EMBEDDING MODEL
# ============================================================

print(
    "\nLoading AI embedding model..."
)

model = SentenceTransformer(
    EMBEDDING_MODEL
)

print(
    "AI model loaded successfully."
)


# ============================================================
# 4. FIND RESUMES
# ============================================================

if not os.path.exists(
    RESUME_FOLDER
):

    print(
        f"\nERROR: Resume folder "
        f"'{RESUME_FOLDER}' does not exist."
    )

    raise SystemExit


resume_files = [

    file

    for file in os.listdir(
        RESUME_FOLDER
    )

    if file.lower().endswith(".pdf")
]


print(
    f"\nFound {len(resume_files)} resumes."
)


if not resume_files:

    print(
        "\nNo PDF resumes found."
    )

    raise SystemExit


# ============================================================
# 5. PROCESS RESUMES
# ============================================================

results = []

failed_files = []


for file in resume_files:

    print(
        f"\nProcessing: {file}"
    )

    try:

        file_path = os.path.join(
            RESUME_FOLDER,
            file
        )

        # ----------------------------------------------------
        # Extract resume
        # ----------------------------------------------------

        resume_text = extract_pdf_text(
            file_path
        )

        if not resume_text.strip():

            print(
                "WARNING: Empty resume."
            )

            failed_files.append(
                file
            )

            continue

        # ----------------------------------------------------
        # Extract skills
        # ----------------------------------------------------

        resume_skills = extract_skills(
            resume_text
        )

        # ----------------------------------------------------
        # Basic skill matching
        # ----------------------------------------------------

        skill_result = calculate_skill_scores(

            required_skills,

            preferred_skills,

            resume_skills
        )

        # ----------------------------------------------------
        # Critical skills
        # ----------------------------------------------------

        critical_result = (
            calculate_critical_skill_score(

                required_skills,

                resume_skills
            )
        )

        # ----------------------------------------------------
        # Supporting skills
        # ----------------------------------------------------

        supporting_result = (
            calculate_supporting_skill_score(

                required_skills,

                preferred_skills,

                resume_skills,

                critical_result
            )
        )

        # ----------------------------------------------------
        # Semantic similarity
        # ----------------------------------------------------

        semantic_score = (
            calculate_semantic_similarity(

                model,

                jd,

                resume_text
            )
        )

        # ----------------------------------------------------
        # Experience
        # ----------------------------------------------------

        (
            experience_score,
            experience_years
        ) = calculate_experience_score(

            resume_text,

            jd
        )

        # ----------------------------------------------------
        # Education
        # ----------------------------------------------------

        (
            education_score,
            education
        ) = calculate_education_score(

            resume_text,

            jd
        )

        # ----------------------------------------------------
        # Final score
        # ----------------------------------------------------

        final_score = calculate_final_score(

            critical_skill_score=
                critical_result[
                    "critical_score"
                ],

            supporting_skill_score=
                supporting_result[
                    "supporting_score"
                ],

            semantic_score=
                semantic_score,

            education_score=
                education_score,

            experience_score=
                experience_score
        )

        # ----------------------------------------------------
        # Decision
        # ----------------------------------------------------

        decision = get_decision(
            final_score
        )

        # ----------------------------------------------------
        # Save result
        # ----------------------------------------------------

        results.append({

            "candidate":
                file,

            "final_score":
                float(final_score),

            "decision":
                decision,

            # Critical
            "critical_score":
                float(
                    round(
                        critical_result[
                            "critical_score"
                        ],
                        2
                    )
                ),

            "critical_required":
                critical_result[
                    "critical_required"
                ],

            "critical_matched":
                critical_result[
                    "critical_matched"
                ],

            "critical_missing":
                critical_result[
                    "critical_missing"
                ],

            # Supporting
            "supporting_score":
                float(
                    round(
                        supporting_result[
                            "supporting_score"
                        ],
                        2
                    )
                ),

            "supporting_required":
                supporting_result[
                    "supporting_required"
                ],

            "supporting_required_matched":
                supporting_result[
                    "supporting_required_matched"
                ],

            "supporting_required_missing":
                supporting_result[
                    "supporting_required_missing"
                ],

            # Compatibility
            "skill_score":
                float(
                    skill_result[
                        "skill_score"
                    ]
                ),

            "required_score":
                float(
                    skill_result[
                        "required_score"
                    ]
                ),

            "preferred_score":
                float(
                    skill_result[
                        "preferred_score"
                    ]
                ),

            # Semantic
            "semantic_score":
                float(
                    round(
                        semantic_score,
                        2
                    )
                ),

            # Experience
            "experience_score":
                float(
                    round(
                        experience_score,
                        2
                    )
                ),

            "experience_years":
                float(
                    experience_years
                ),

            # Education
            "education_score":
                float(
                    round(
                        education_score,
                        2
                    )
                ),

            "education":
                education,

            # Required
            "required_matched":
                skill_result[
                    "required_matched"
                ],

            "required_missing":
                skill_result[
                    "required_missing"
                ],

            # Preferred
            "preferred_matched":
                skill_result[
                    "preferred_matched"
                ],

            "preferred_missing":
                skill_result[
                    "preferred_missing"
                ]
        })

    except Exception as error:

        print(
            f"ERROR processing {file}: "
            f"{error}"
        )

        failed_files.append(
            file
        )


# ============================================================
# 6. CHECK RESULTS
# ============================================================

if not results:

    print(
        "\nNo valid resumes were processed."
    )

    raise SystemExit


# ============================================================
# 7. RANK
# ============================================================

results.sort(

    key=lambda x:
        x["final_score"],

    reverse=True
)


# ============================================================
# 8. RULE-BASED EXPLANATION
# ============================================================

for result in results:

    try:

        result["explanation"] = (
            generate_explanation(
                result
            )
        )

    except Exception as error:

        print(
            f"WARNING: Explanation failed "
            f"for {result['candidate']}: "
            f"{error}"
        )

        result["explanation"] = {}


# ============================================================
# 9. DISPLAY SCREENING RESULTS
# ============================================================

display_results(
    results
)


# ============================================================
# 10. LLM REASONING
# ============================================================

print(
    "\n" + "=" * 90
)

print(
    "                 GENERATING AI REASONING"
)

print(
    "=" * 90
)


top_candidates = results[
    :LLM_TOP_CANDIDATES
]


for result in top_candidates:

    print(
        f"\nGenerating explanation for: "
        f"{result['candidate']}"
    )

    resume_path = os.path.join(

        RESUME_FOLDER,

        result["candidate"]
    )

    try:

        resume_text = extract_pdf_text(
            resume_path
        )

        explanation = (
            generate_llm_explanation(

                jd,

                result,

                resume_text
            )
        )

        result[
            "llm_explanation"
        ] = explanation

        print(
            "AI explanation generated."
        )

    except Exception as error:

        print(
            f"WARNING: LLM explanation failed: "
            f"{error}"
        )

        result[
            "llm_explanation"
        ] = {

            "summary":
                "LLM explanation unavailable.",

            "strengths": [],

            "gaps": [],

            "recommendation":
                "Manual review recommended."
        }


# ============================================================
# 11. DISPLAY AI REASONING
# ============================================================

print(
    "\n" + "=" * 90
)

print(
    "                 AI HIRING REASONING"
)

print(
    "=" * 90
)


for rank, result in enumerate(
    top_candidates,
    start=1
):

    explanation = result.get(
        "llm_explanation",
        {}
    )

    print(
        "\n" + "-" * 90
    )

    print(
        f"Rank {rank}: "
        f"{result['candidate']}"
    )

    print(
        f"Score: "
        f"{result['final_score']:.2f}%"
    )

    print(
        f"Decision: "
        f"{result['decision']}"
    )

    print(
        "\nScore Breakdown:"
    )

    print(
        f"  Critical Skills : "
        f"{result['critical_score']:.2f}%"
    )

    print(
        f"  Supporting      : "
        f"{result['supporting_score']:.2f}%"
    )

    print(
        f"  Semantic        : "
        f"{result['semantic_score']:.2f}%"
    )

    print(
        f"  Experience      : "
        f"{result['experience_score']:.2f}%"
    )

    print(
        f"  Education       : "
        f"{result['education_score']:.2f}%"
    )

    print("\nSummary:")

    print(
        explanation.get(
            "summary",
            ""
        )
    )

    print("\nStrengths:")

    for strength in explanation.get(
        "strengths",
        []
    ):

        print(
            f"  ✓ {strength}"
        )

    print("\nGaps:")

    for gap in explanation.get(
        "gaps",
        []
    ):

        print(
            f"  - {gap}"
        )

    print("\nRecommendation:")

    print(
        explanation.get(
            "recommendation",
            ""
        )
    )


# ============================================================
# 12. SAVE CSV
# ============================================================

csv_path = save_csv(

    results,

    OUTPUT_FOLDER
)


# ============================================================
# 13. SAVE JSON
# ============================================================

json_path = save_json(

    results,

    OUTPUT_FOLDER
)


# ============================================================
# 14. SUMMARY
# ============================================================

total_resumes = len(
    resume_files
)

processed_resumes = len(
    results
)

failed_resumes = len(
    failed_files
)

strong_matches = sum(

    result["decision"]
    == "Strong Match"

    for result in results
)

good_matches = sum(

    result["decision"]
    == "Good Match"

    for result in results
)

moderate_matches = sum(

    result["decision"]
    == "Moderate Match"

    for result in results
)

weak_matches = sum(

    result["decision"]
    == "Weak Match"

    for result in results
)


print(
    "\n" + "=" * 90
)

print(
    "                 PROCESSING SUMMARY"
)

print(
    "=" * 90
)

print(
    f"\nTotal resumes found     : "
    f"{total_resumes}"
)

print(
    f"Successfully processed  : "
    f"{processed_resumes}"
)

print(
    f"Failed                  : "
    f"{failed_resumes}"
)

print(
    f"Strong Match            : "
    f"{strong_matches}"
)

print(
    f"Good Match              : "
    f"{good_matches}"
)

print(
    f"Moderate Match          : "
    f"{moderate_matches}"
)

print(
    f"Weak Match              : "
    f"{weak_matches}"
)


if failed_files:

    print(
        "\nFailed files:"
    )

    for file in failed_files:

        print(
            f"  - {file}"
        )


print(
    "\n" + "=" * 90
)

print(
    "Screening completed successfully."
)

print(
    "=" * 90
)

print(
    f"\nCSV  : {csv_path}"
)

print(
    f"JSON : {json_path}"
)